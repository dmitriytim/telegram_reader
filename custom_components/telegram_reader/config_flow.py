from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
import voluptuous as vol

class MyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}
        if user_input is not None:
            # В этом месте вы можете добавить код для авторизации в Telegram
            return await self.async_step_channels(user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("api_id"): str,
                    vol.Required("api_hash"): str,
                    vol.Required("phone"): str,
                }
            ),
            errors=errors,
        )

    async def async_step_channels(self, user_input=None) -> FlowResult:
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="Telegram Channels", data=user_input)

        return self.async_show_form(
            step_id="channels",
            data_schema=vol.Schema(
                {
                    vol.Required("channels"): str,
                }
            ),
            errors=errors,
        )
