from pyrogram import filters, Client, enums
from pyrogram.types import Message

from pyrogram.handlers import MessageHandler
from tauon import tauon


def on_msg(**kwargs):
    pattern: str = kwargs.get("pattern", None)
    incoming: bool = kwargs.get("incoming", False)
    outgoing: bool = kwargs.get("outgoing", True)
    group: bool = kwargs.get("group", True)
    private: bool = kwargs.get("private", True)
    admin: bool = kwargs.get("admin", True)

    def decorator(func):
        async def wrapper(client: Client, message: Message):
            me = await client.get_me()
            trigger = False
            if group:
                if enums.chat_type.ChatType.GROUP == message.chat.type:
                    trigger = True
            if private:
                if enums.chat_type.ChatType.PRIVATE == message.chat.type:
                    trigger = True
            if admin:
                if message.from_user.id == me.id:
                    trigger = True

            if trigger:
                args = []
                args.append(client)
                args.append(message)
            return await func(*args)

        filter = filters.create(lambda _, __, ___: True)
        if pattern:
            filter &= filters.regex(f"^[\./!]{pattern}$")
        if outgoing and not incoming:
            filter &= filters.me & ~filters.incoming
        if not outgoing and incoming:
            filter &= filters.incoming & ~filters.me
        else:
            filter &= filters.me | filters.incoming

        tauon.add_handler(MessageHandler(wrapper, filter))

    return decorator
