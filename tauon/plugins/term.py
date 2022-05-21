import subprocess

from pyrogram import Client, filters
from pyrogram.types import Message
from tauon.core.handler import on_msg
from tauon import HELP

HELP["term"] = {"term": ".term <kod>"}


@on_msg(pattern="term (.*)")
async def term_(client: Client, message: Message) -> None:
    user = message.from_user.username
    await message.edit_text("Alınıyor")
    code = " ".join(message.text.split()[1:])
    try:
        output = subprocess.getoutput(code)
        await message.edit_text(f"`{user}:~#` `{code}`\n\n`{output} `")
    except Exception as e:
        await message.edit_text(f"`Hata: {e}`")
