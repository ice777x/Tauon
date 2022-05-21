from pyrogram import Client, filters
from pyrogram.types import Message
from asyncio import sleep


class Conversation:
    def __init__(self, client: Client, text,chat_id, forward_chat_id, message_id):
        self.text =text
        self._client = client
        self._chat = chat_id
        self.forward_chat_id = forward_chat_id or None
        self._message_id = message_id
        self.message = None

    async def create_conversation(self):
        mesaj = await self.send_msg()
        x = 0
        while x < 40:
            await sleep(0.7)
            async for i in self._client.get_chat_history(
                self.forward_chat_id, limit=1,offset=0
            ):
                x += 1
                if i.text == mesaj.text:
                    continue
                else:
                    self.message = i
                    break
            if self.message != None:
                break
        return self.message

    async def forward_message(self):
        msg = await self._client.forward_messages(
            chat_id=self.forward_chat_id,
            message_ids=self._message_id,
            from_chat_id=self._chat,
        )
        return msg
    
    async def send_msg(self):
        mesaj = await self._client.send_message(
            chat_id=self.forward_chat_id,
            text=self.text,
            reply_to_message_id=self._message_id,
        )
        return mesaj