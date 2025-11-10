
import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_TCP_PORT, CONF_EVENT_TYPE

class TcpToEventConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="TCP to Event Converter", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_TCP_PORT, default=54321): int,
                vol.Required(CONF_EVENT_TYPE, default="tcp_event"): str,
            })
        )
