
import asyncio
import logging
from typing import Optional, Set
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

BUFFER_SIZE = 1024
SHUTDOWN_TIMEOUT = 5.0

class TCPServer:
    def __init__(self, hass: HomeAssistant, tcp_port: int, event_type: str) -> None:
        self.hass = hass
        self.tcp_port = tcp_port
        self.event_type = event_type
        self.server: Optional[asyncio.Server] = None
        self.client_tasks: Set[asyncio.Task] = set()

    async def start(self) -> None:
        """Start the TCP server."""
        try:
            self.server = await asyncio.start_server(
                self.handle_connection, "0.0.0.0", self.tcp_port
            )
            _LOGGER.info("TCP Server started on port %d", self.tcp_port)
        except Exception as e:
            _LOGGER.error("Failed to start TCP server on port %d: %s", self.tcp_port, e)
            raise

    async def stop(self, event=None) -> None:
        """Stop the server and cancel all client connections."""
        if self.server is None:
            return  # Already stopped

        server = self.server
        self.server = None  # Mark as stopped to prevent double-stop

        # First, stop accepting new connections
        server.close()
        _LOGGER.debug("TCP Server closed to new connections")

        # Cancel all active client connection tasks
        if self.client_tasks:
            _LOGGER.debug("Cancelling %d active client connections", len(self.client_tasks))
            for task in self.client_tasks:
                if not task.done():
                    task.cancel()

            # Wait for all client tasks to finish (with timeout)
            try:
                await asyncio.wait_for(
                    asyncio.gather(*self.client_tasks, return_exceptions=True),
                    timeout=SHUTDOWN_TIMEOUT
                )
            except asyncio.TimeoutError:
                _LOGGER.warning(
                    "Some client connections did not close within %s seconds",
                    SHUTDOWN_TIMEOUT
                )

        # Wait for server to fully close (with timeout)
        try:
            await asyncio.wait_for(server.wait_closed(), timeout=SHUTDOWN_TIMEOUT)
        except asyncio.TimeoutError:
            _LOGGER.warning(
                "Server did not close within %s seconds",
                SHUTDOWN_TIMEOUT
            )

        _LOGGER.info("TCP Server stopped")

    async def handle_connection(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        """Handle a client connection - wrapper that tracks the task."""
        task = asyncio.current_task()
        if task:
            self.client_tasks.add(task)

        try:
            await self._handle_connection_impl(reader, writer)
        finally:
            if task:
                self.client_tasks.discard(task)

    async def _handle_connection_impl(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        """Internal connection handler implementation."""
        addr = writer.get_extra_info("peername")
        _LOGGER.info("Connection established from %s", addr)

        try:
            while True:
                data = await reader.read(BUFFER_SIZE)
                if not data:
                    _LOGGER.info("Connection from %s closed by peer", addr)
                    break

                try:
                    raw_payload = data.decode("utf-8").strip()
                except UnicodeDecodeError:
                    _LOGGER.warning("Received non-UTF-8 data from %s", addr)
                    continue

                _LOGGER.debug("Received raw payload: %s", raw_payload)

                parts = raw_payload.split(":")
                if len(parts) == 3:
                    device_id, button_id, action_type = parts
                    event_data = {
                        "device_id": device_id,
                        "button_id": button_id,
                        "action": action_type,
                    }
                    _LOGGER.info("Firing event %s with data: %s", self.event_type, event_data)
                    self.hass.bus.async_fire(self.event_type, event_data)
                else:
                    _LOGGER.warning(
                        "Invalid message format received from %s: %s", addr, raw_payload
                    )

        except asyncio.CancelledError:
            _LOGGER.debug("Connection handler for %s cancelled", addr)
            raise  # Re-raise to properly propagate cancellation
        except Exception as e:
            _LOGGER.error("Unexpected error handling connection from %s: %s", addr, e)
        finally:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception as e:
                _LOGGER.debug("Error closing writer for %s: %s", addr, e)
            _LOGGER.info("Connection with %s closed", addr)
