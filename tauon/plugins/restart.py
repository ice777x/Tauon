from tauon.core.handler import on_msg
from pyrogram import Client
from pyrogram.types import Message
import os
import psutil
import sys
import importlib


@on_msg(pattern="restart")
async def restart(client: Client, message: Message):
    await message.edit_text("`Bot yeniden başlatılıyor..`")
    await client.stop()
    c_p = psutil.Process(os.getpid())
    for handler in c_p.open_files() + c_p.connections():
        os.close(handler.fd)
    os.execl(sys.executable, "main.py")


@on_msg(pattern="reload")
async def reload(_, message: Message):
    modules = os.listdir("tauon/plugins")
    for i in modules:
        if i.endswith(".py"):
            importlib.reload(importlib.import_module("tauon.plugins." + i[:-3]))
    await message.edit_text("`Modüller yeniden yüklendi.`")
    # await message.edit_text(f"`Hata: {e.args}`")
