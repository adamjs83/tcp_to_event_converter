
import asyncio
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN, CONF_TCP_PORT, CONF_EVENT_TYPE
from .tcp_server import TCPServer

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up TCP to Event Converter from a config entry."""
    tcp_port = entry.data[CONF_TCP_PORT]
    event_type = entry.data[CONF_EVENT_TYPE]

    server = TCPServer(hass, tcp_port, event_type)

    try:
        await server.start()
    except Exception as e:
        _LOGGER.error("Failed to setup TCP to Event Converter: %s", e)
        return False

    hass.data[DOMAIN] = server
    _LOGGER.info("TCP to Event Converter setup complete on port %d", tcp_port)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload the TCP to Event Converter integration."""
    server = hass.data.pop(DOMAIN, None)
    if server:
        try:
            await server.stop()
        except Exception as e:
            _LOGGER.error("Error stopping TCP server during unload: %s", e)
            return False

    _LOGGER.info("TCP to Event Converter unloaded successfully")
    return True
