"""TCP Server for receiving and converting messages to Home Assistant events."""

import asyncio
import logging
import re
from typing import Optional, Set

from homeassistant.core import HomeAssistant

from .const import (
    EXPECTED_MESSAGE_PARTS,
    MAX_FIELD_LENGTH,
    FIELD_VALIDATION_PATTERN,
    MAX_CONNECTIONS,
    READ_TIMEOUT,
)

_LOGGER = logging.getLogger(__name__)

# Buffer size for reading from TCP connections
BUFFER_SIZE: int = 1024
# Timeout for graceful shutdown
SHUTDOWN_TIMEOUT: float = 5.0


class TCPServer:
    """TCP Server that receives messages and fires Home Assistant events.

    This server listens for TCP connections and processes incoming messages
    in the format: device_id:button_id:action

    Each valid message is converted to a Home Assistant event with validated
    and sanitized data.
    """

    def __init__(self, hass: HomeAssistant, tcp_port: int, event_type: str) -> None:
        """Initialize the TCP server.

        Args:
            hass: Home Assistant instance
            tcp_port: Port number to listen on
            event_type: Event type to fire for incoming messages
        """
        self.hass = hass
        self.tcp_port = tcp_port
        self.event_type = event_type
        self.server: Optional[asyncio.Server] = None
        self.client_tasks: Set[asyncio.Task] = set()
        self._connection_count: int = 0
        self._field_pattern = re.compile(FIELD_VALIDATION_PATTERN)

    async def start(self) -> None:
        """Start the TCP server.

        Raises:
            OSError: If the port is already in use or cannot be bound
            asyncio.TimeoutError: If server startup times out
        """
        try:
            self.server = await asyncio.start_server(
                self.handle_connection, "0.0.0.0", self.tcp_port
            )
            _LOGGER.info("TCP Server started on port %d", self.tcp_port)
        except OSError as e:
            _LOGGER.error(
                "Failed to start TCP server on port %d: %s (errno: %d)",
                self.tcp_port, e, e.errno if hasattr(e, 'errno') else -1
            )
            raise
        except asyncio.TimeoutError as e:
            _LOGGER.error("Timeout starting TCP server on port %d", self.tcp_port)
            raise
        except Exception as e:
            _LOGGER.error(
                "Unexpected error starting TCP server on port %d: %s",
                self.tcp_port, e
            )
            raise

    async def stop(self) -> None:
        """Stop the server and cancel all client connections.

        Performs graceful shutdown by:
        1. Stopping acceptance of new connections
        2. Cancelling all active client tasks
        3. Waiting for tasks to complete (with timeout)
        4. Closing the server socket
        """
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
        """Handle a client connection - wrapper that tracks the task.

        This method enforces connection limits and tracks active connections.

        Args:
            reader: Stream reader for receiving data
            writer: Stream writer for sending data (currently unused)
        """
        # Check connection limit before accepting
        if self._connection_count >= MAX_CONNECTIONS:
            addr = writer.get_extra_info("peername")
            _LOGGER.warning(
                "Connection limit reached (%d/%d), rejecting connection from %s",
                self._connection_count, MAX_CONNECTIONS, addr
            )
            try:
                writer.close()
                await writer.wait_closed()
            except Exception as e:
                _LOGGER.debug("Error closing rejected connection: %s", e)
            return

        self._connection_count += 1
        task = asyncio.current_task()
        if task:
            self.client_tasks.add(task)

        try:
            await self._handle_connection_impl(reader, writer)
        finally:
            self._connection_count -= 1
            if task:
                self.client_tasks.discard(task)

    async def _handle_connection_impl(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        """Internal connection handler implementation.

        Processes incoming messages with validation and sanitization:
        - Enforces read timeouts
        - Validates message format
        - Sanitizes field contents
        - Fires Home Assistant events

        Args:
            reader: Stream reader for receiving data
            writer: Stream writer for connection management
        """
        addr = writer.get_extra_info("peername")
        _LOGGER.info("Connection established from %s", addr)

        try:
            while True:
                # Read with timeout to prevent hung connections
                try:
                    data = await asyncio.wait_for(
                        reader.read(BUFFER_SIZE),
                        timeout=READ_TIMEOUT
                    )
                except asyncio.TimeoutError:
                    _LOGGER.debug(
                        "Read timeout (%s seconds) from %s, closing connection",
                        READ_TIMEOUT, addr
                    )
                    break

                if not data:
                    _LOGGER.info("Connection from %s closed by peer", addr)
                    break

                # Decode and validate UTF-8
                try:
                    raw_payload = data.decode("utf-8").strip()
                except UnicodeDecodeError:
                    _LOGGER.warning("Received non-UTF-8 data from %s", addr)
                    continue

                # Sanitize for logging to prevent log injection
                safe_payload = self._sanitize_for_log(raw_payload)
                _LOGGER.debug("Received raw payload from %s: %s", addr, safe_payload)

                # Process the message
                self._process_message(raw_payload, addr)

        except asyncio.CancelledError:
            _LOGGER.debug("Connection handler for %s cancelled", addr)
            raise  # Re-raise to properly propagate cancellation
        except ConnectionError as e:
            _LOGGER.warning("Connection error from %s: %s", addr, e)
        except OSError as e:
            _LOGGER.warning("OS error handling connection from %s: %s", addr, e)
        except Exception as e:
            _LOGGER.error("Unexpected error handling connection from %s: %s", addr, e)
        finally:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception as e:
                _LOGGER.debug("Error closing writer for %s: %s", addr, e)
            _LOGGER.info("Connection with %s closed", addr)

    def _process_message(self, raw_payload: str, addr: tuple) -> None:
        """Process and validate an incoming message.

        Expected format: device_id:button_id:action

        Args:
            raw_payload: The raw message string
            addr: Client address for logging
        """
        # Split with maxsplit to handle potential extra colons in data
        parts = raw_payload.split(":", maxsplit=EXPECTED_MESSAGE_PARTS - 1)

        if len(parts) != EXPECTED_MESSAGE_PARTS:
            _LOGGER.warning(
                "Invalid message format from %s: expected %d parts, got %d: %s",
                addr, EXPECTED_MESSAGE_PARTS, len(parts),
                self._sanitize_for_log(raw_payload)
            )
            return

        device_id, button_id, action_type = parts

        # Validate and sanitize each field
        try:
            validated_device_id = self._validate_field(device_id, "device_id")
            validated_button_id = self._validate_field(button_id, "button_id")
            validated_action = self._validate_field(action_type, "action")
        except ValueError as e:
            _LOGGER.warning("Message validation failed from %s: %s", addr, e)
            return

        # Create event data and fire event
        event_data = {
            "device_id": validated_device_id,
            "button_id": validated_button_id,
            "action": validated_action,
        }

        _LOGGER.info(
            "Firing event %s with data: %s",
            self.event_type, event_data
        )
        self.hass.bus.async_fire(self.event_type, event_data)

    def _validate_field(self, field: str, field_name: str) -> str:
        """Validate and sanitize a message field.

        Validation rules:
        - Maximum length of MAX_FIELD_LENGTH characters
        - Only alphanumeric, underscore, and hyphen characters
        - Pattern: ^[a-zA-Z0-9_-]+$

        Args:
            field: The field value to validate
            field_name: Name of the field for error messages

        Returns:
            The validated field value (stripped)

        Raises:
            ValueError: If validation fails
        """
        # Strip whitespace
        field = field.strip()

        # Check for empty field
        if not field:
            raise ValueError(f"{field_name} cannot be empty")

        # Check maximum length
        if len(field) > MAX_FIELD_LENGTH:
            raise ValueError(
                f"{field_name} exceeds maximum length "
                f"({len(field)} > {MAX_FIELD_LENGTH}): {field[:20]}..."
            )

        # Validate character set
        if not self._field_pattern.match(field):
            raise ValueError(
                f"{field_name} contains invalid characters "
                f"(must match {FIELD_VALIDATION_PATTERN}): {field[:20]}..."
            )

        return field

    @staticmethod
    def _sanitize_for_log(message: str) -> str:
        """Sanitize a message for safe logging.

        Removes control characters and limits length to prevent:
        - Log injection attacks
        - Log file bloat
        - Terminal control sequence abuse

        Args:
            message: The message to sanitize

        Returns:
            Sanitized message safe for logging
        """
        # Remove control characters (except tab and newline, then replace those too)
        sanitized = "".join(
            char if char.isprintable() or char in ("\t", "\n") else "?"
            for char in message
        )

        # Replace tabs and newlines with spaces to prevent log injection
        sanitized = sanitized.replace("\t", " ").replace("\n", " ").replace("\r", " ")

        # Limit length for logging
        max_log_length = 200
        if len(sanitized) > max_log_length:
            sanitized = sanitized[:max_log_length] + "... (truncated)"

        return sanitized
