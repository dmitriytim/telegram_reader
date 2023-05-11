from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .telegram_reader import TelegramReader  # Убедитесь, что TelegramReader находится в том же каталоге
from homeassistant import config_entries
from .config_flow import MyConfigFlow

DOMAIN = "telegram_reader"

async def async_setup(hass, config):
    hass.config_entries.async_register_flow_handler(DOMAIN, MyConfigFlow)
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    # Создаем экземпляр нашего компонента с данными из настроек пользователя
    telegram_reader = TelegramReader(entry.data)

    # Устанавливаем экземпляр компонента для использования в других частях нашей интеграции
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = telegram_reader

    # Добавляем сенсоры для нашего компонента
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    # Возвращает True, если инициализация прошла успешно
    return True
