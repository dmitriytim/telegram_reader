from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetHistoryRequest

class TelegramReader:
    def __init__(self, config):
        self.api_id = config["api_id"]
        self.api_hash = config["api_hash"]
        self.phone = config["phone"]
        self.channels = config["channels"].split(',')

        self.client = TelegramClient(self.phone, self.api_id, self.api_hash)

    async def connect(self):
        await self.client.connect()

    async def get_messages(self, channel):
        # Получаем полную информацию о канале
        full = await self.client(GetFullChannelRequest(channel))
        # Получаем историю сообщений канала
        messages = await self.client(GetHistoryRequest(
            peer=full.chats[0],
            limit=10,  # количество сообщений для извлечения
            offset_id=0,
            offset_date=None,
            add_offset=0,
            max_id=0,
            min_id=0,
            hash=0
        ))
        return messages.messages  # возвращает список объектов Message
