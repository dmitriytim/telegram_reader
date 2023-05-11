from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
import voluptuous as vol
DOMAIN = "telegram_reader"

class MyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        self._user_input = None

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}
        if user_input is not None:
            # В этом месте вы можете добавить код для авторизации в Telegram
            self._user_input = user_input  # Сохраняем данные от пользователя
            return await self.async_step_channels()

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
            self._user_input.update(user_input)  # Объединяем данные от пользователя с новыми данными
            return self.async_create_entry(title="Telegram Channels", data=self._user_input)

        return self.async_show_form(
            step_id="channels",
            data_schema=vol.Schema(
                {
                    vol.Required("channels"): str,
                }
            ),
            errors=errors,
        )
