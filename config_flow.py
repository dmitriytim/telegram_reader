from homeassistant import config_entries

class MyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="My Integration", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("api_id"): str,
                    vol.Required("api_hash"): str,
                    vol.Required("phone"): str,
                    vol.Required("channels"): str,
                }
            ),
        )
