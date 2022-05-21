from tauon.core.handler import on_msg
from pyrogram.types import Message


@on_msg(pattern="alive")
async def alive(_, message: Message):
    await message.edit("`Tau ,)`")
