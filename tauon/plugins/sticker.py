from pyrogram import Client
from pyrogram.types import Message
from tauon.core.handler import on_msg
from tauon import HELP
import asyncio
from tauon.core.conversation import Conversation

HELP["sticker"] = {"q": "quotly <yanıt> - Sticker'a cevirir."}


@on_msg(pattern="(q|quotly) ?(.*)")
async def quotly(client: Client, message: Message):
    await message.edit_text("`Sticker'a çevriliyor...`")
    chat_id = message.chat.id
    messages = await Conversation(
        text = message.reply_to_message.text,
        client=client,
        chat_id=chat_id,
        forward_chat_id="@QuotLyBot",
        message_id=message.reply_to_message.id,
    ).create_conversation()
    await message.delete()
    await client.send_sticker(chat_id,messages.sticker.file_id)