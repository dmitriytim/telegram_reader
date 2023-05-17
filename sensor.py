from homeassistant.helpers.entity import Entity

class MySensor(Entity):
    def __init__(self, api_id, api_hash, phone, channels):
        self._state = None
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.channels = channels

    @property
    def state(self):
        return self._state

    async def async_update(self):
        from telethon import TelegramClient
        async with TelegramClient('anon', self.api_id, self.api_hash) as client:
            for channel in self.channels.split(','):
                messages = await client.get_messages(channel, limit=10)
                self._state = [msg.message for msg in messages]
