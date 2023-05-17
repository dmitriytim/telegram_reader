from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .telegram_reader import TelegramReader  # Убедитесь, что TelegramReader находится в том же каталоге
from homeassistant import config_entries
from .config_flow import MyConfigFlow


DOMAIN = "telegram_reader"

async def async_setup(hass, config):
    hass.data[DOMAIN] = {}
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data[DOMAIN][entry.entry_id] = TelegramReader(entry.data)
    return True

