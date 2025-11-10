
import asyncio
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EVENT_HOMEASSISTANT_STOP
from homeassistant.core import HomeAssistant
from .const import DOMAIN, CONF_TCP_PORT, CONF_EVENT_TYPE
from .tcp_server import TCPServer

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    tcp_port = entry.data[CONF_TCP_PORT]
    event_type = entry.data[CONF_EVENT_TYPE]

    server = TCPServer(hass, tcp_port, event_type)
    hass.data[DOMAIN] = server
    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, server.stop)

    await server.start()
    _LOGGER.info("TCP to Event Converter setup complete.")
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    server = hass.data.pop(DOMAIN, None)
    if server:
        await server.stop()
    return True
