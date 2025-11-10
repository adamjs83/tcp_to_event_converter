
import asyncio
import logging
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

class TCPServer:
    def __init__(self, hass: HomeAssistant, tcp_port: int, event_type: str) -> None:
        self.hass = hass
        self.tcp_port = tcp_port
        self.event_type = event_type
        self.server = None

    async def start(self) -> None:
        try:
            self.server = await asyncio.start_server(self.handle_connection, "0.0.0.0", self.tcp_port)
            _LOGGER.info("TCP Server started on port %d", self.tcp_port)
        except Exception as e:
            _LOGGER.error("Failed to start TCP server on port %d: %s", self.tcp_port, e)

    async def stop(self, event=None) -> None:
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            _LOGGER.info("TCP Server stopped")

    async def handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        addr = writer.get_extra_info("peername")
        _LOGGER.info("Connection established from %s", addr)

        try:
            while True:
                data = await reader.read(1024)
                if not data:
                    _LOGGER.info("Connection from %s closed by peer", addr)
                    break

                raw_payload = data.decode("utf-8").strip()
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
                    _LOGGER.warning("Invalid message format received from %s: %s", addr, raw_payload)

        except asyncio.CancelledError:
            pass
        except Exception as e:
            _LOGGER.error("Unexpected error handling connection from %s: %s", addr, e)
        finally:
            writer.close()
            await writer.wait_closed()
            _LOGGER.info("Connection with %s closed", addr)
