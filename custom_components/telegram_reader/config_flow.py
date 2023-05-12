from homeassistant import config_entries, exceptions
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
import voluptuous as vol
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
import logging
from telethon import types

_LOGGER = logging.getLogger(__name__)
DOMAIN = "telegram_reader"
class MyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL


    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}
        if user_input is not None:
            self.data = user_input
            self.api_id = user_input["api_id"]
            self.api_hash = user_input["api_hash"]
            self.phone = user_input["phone"]

            self.client = TelegramClient('anon', self.api_id, self.api_hash)
            await self.client.connect()
            if await self.client.is_user_authorized():
                return await self.async_step_channels()

            if not await self.client.is_user_authorized():
                await self.client.send_code_request(self.phone)
                return await self.async_step_verify()
            if self._async_current_entries():
                # Если уже существует запись, взять данные из нее
                entry = self._async_current_entries()[0]
                self.api_id = entry.data["api_id"]
                self.api_hash = entry.data["api_hash"]
                self.phone = entry.data["phone"]

                # Если уже есть сохраненная конфигурация, отобразить ее в форме
                return self.async_show_form(
                    step_id="user",
                    data_schema=vol.Schema(
                        {
                            vol.Required("api_id", default=self.api_id): str,
                            vol.Required("api_hash", default=self.api_hash): str,
                            vol.Required("phone", default=self.phone): str,
                        }
                    ),
                )

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

    async def async_step_verify(self, user_input=None) -> FlowResult:
        errors = {}
        if user_input is not None:
            try:
                self.verification_code = user_input["verification_code"]
                await self.client.sign_in(self.phone, self.verification_code)
                return await self.async_step_channels()
            except SessionPasswordNeededError:
                return await self.async_step_password()
            except Exception as e:
                errors["base"] = "unknown"
                _LOGGER.error(f"Failed to process verification code: {e}")

        return self.async_show_form(
            step_id="verify",
            data_schema=vol.Schema(
                {
                    vol.Required("verification_code"): str,
                }
            ),
            errors=errors,
        )


    async def async_step_password(self, user_input=None):
        errors = {}
        if user_input is not None:
            self.data.update(user_input)
            await self.client.sign_in(password=user_input["password"])
            return await self.async_step_channels()

        return self.async_show_form(
            step_id="password",
            data_schema=vol.Schema({vol.Required("password"): str}),
            errors=errors,
        )

    async def async_step_channels(self, user_input=None):
        errors = {}
        if user_input is not None:
            self.channels = [id for id, selected in user_input["channels"].items() if selected]
            return self.async_create_entry(
                title="Telegram Channels",
                data={
                    "api_id": self.api_id,
                    "api_hash": self.api_hash,
                    "phone": self.phone,
                    "channels": self.channels,
                },
            )

        dialogs = await self.client.get_dialogs()
        channels = {dialog.entity.id: dialog.entity.title for dialog in dialogs if isinstance(dialog.entity, types.Channel)}

        return self.async_show_form(
            step_id="channels",
            data_schema=vol.Schema(
                {
                    vol.Required("channels", default=self.channels): vol.Schema(
                        {channel_id: str for channel_id in channels.keys()}
                    ),
                }
            ),
            errors=errors,
        )



