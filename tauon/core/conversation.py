from pyrogram import Client, filters
from pyrogram.types import Message
from asyncio import sleep


class Conversation:
    def __init__(self, client: Client, chat_id, forward_chat_id, message_ids):
        self._client = client
        self._chat = chat_id
        self.forward_chat_id = forward_chat_id
        self._message_ids = message_ids

    async def create_conversation(self):
        mesaj = await self.forward_message()
        x = 0
        messages = []
        while x < 40:
            async for i in self._client.get_chat_history(
                self.forward_chat_id, offset_id=mesaj.id, limit=1
            ):
                if i.text:
                    x += 1
                else:
                    messages.append(i)
                await sleep(0.5)
        return messages

    async def forward_message(self):
        msg = await self._client.forward_messages(
            chat_id=self.forward_chat_id,
            message_ids=self._message_ids,
            from_chat_id=self._chat,
        )
        return msg
