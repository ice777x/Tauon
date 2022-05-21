import asyncio
from pyrogram import Client, errors
from pyrogram.types import Message
from tauon.core.handler import on_msg
from tauon import HELP

HELP["spam"] = {"spam": ".spam <text> - Spam yapar."}


@on_msg(pattern="spam (.*)")
async def spam_(client: Client, message: Message):
    await message.delete()
    metin = message.text.split()
    number = int(metin[1])
    alinacak = " ".join(metin[2:])
    chat_id = message.chat.id
    try:
        if not message.reply_to_message:
            tasks = (asyncio.create_task(message.reply(alinacak)) for i in range(number))
            await asyncio.gather(*tasks)
        else:
            tasks = (
                asyncio.create_task(
                    client.send_message(
                        chat_id, alinacak, reply_to=message.reply_to_message.id
                    )
                )
                for i in range(number)
            )
            await asyncio.gather(*tasks)
    except errors.FloodWait as fw:
        await asyncio.sleep(fw.x)
        await client.send_message(
            f"`{fw.x} saniyeliğine uyutuldun.\nBirdahakine daha dikkatli ol!`"
        )
        return
