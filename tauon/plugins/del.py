from pyrogram import Client, enums
from pyrogram.types import Message
from tauon.core.handler import on_msg
from tauon import HELP

HELP["del"] = {
    "del": ".del <miktar>  - Belirtilen mesajı siler.",
    "delall": ".delall <kullanıcı_adı>  - Belirtilen kullanıcının mesajlarını siler.",
    "delme": ".delme  - Mesajlarınızı siler.",
    "deluser": ".deluser <miktar>  - Belirtilen kullanıcının mesajlarını siler.",
    "tag": ".tag - tüm üyeleri etiketler.",
    "getadmin": ".getadmin - tüm adminleri etiketler.",
}


@on_msg(pattern="veri")
async def ido(client: Client, message: Message):
    if len(str(message)) > 4096:
        await message.delete()
        await client.send_message(chat_id=message.chat.id, text=f"{str(message)[:4096]}")
        await client.send_message(
            chat_id=message.chat.id, text=f"{str(message)[4096:8192]}"
        )
    else:
        await message.edit_text(f"{message}")

    message.continue_propagation()


@on_msg(pattern="delall")
async def delall(client: Client, message: Message):
    await message.delete()
    try:
        if not message.reply_to_message:
            eleman_id = message.text.split(".delall ")[1].strip()
        else:
            eleman_id = message.reply_to_message.from_user.id
    except AttributeError:
        await message.edit_text(HELP["del"]["delall"])
        return
    await client.delete_user_history(chat_id=message.chat.id, user_id=eleman_id)


@on_msg(pattern="del (.*)")
async def del_msg(client: Client, message: Message):
    await message.delete()
    silin = []
    try:
        if len(message.text.split()) > 1 and message.text.split()[1].isnumeric():
            async for i in client.get_chat_history(
                chat_id=message.chat.id, limit=int(message.text.split()[1])
            ):
                silin.append(i.id)
        else:
            silin = message.reply_to_message.id
    except Exception:
        await message.edit_text(HELP["del"]["del"])
        return
    await client.delete_messages(chat_id=message.chat.id, message_ids=silin)


@on_msg(pattern="delme (.*)")
async def delme(client: Client, message: Message):
    try:
        mk = int(message.text.split()[1])
        my_us = message.from_user.username
        i = 1
        messages = []
        async for msg in client.search_messages(chat_id=message.chat.id, from_user=my_us):
            if i > mk + 1:
                break
            messages.append(msg.id)
            i = i + 1
        await client.delete_messages(message.chat.id, messages)
    except Exception:
        await message.edit_text(HELP["del"]["delme"])
        return


@on_msg(pattern="deluser (.*)")
async def del_user(client: Client, message: Message):
    try:
        await message.edit_text("`deleting messages..`")
        mk = int(message.text.split()[1])
        if message.reply_to_message:
            d_m_l = []
            x = 0
            async for msg in client.get_chat_history(
                message.chat.id,
                offset_id=message.reply_to_message.id + 1,
            ):
                if x < mk:
                    if msg.from_user.id == message.reply_to_message.from_user.id:
                        d_m_l.append(msg.id)
                    else:
                        mk += 1
                    x += 1
                else:
                    break
            await client.delete_messages(chat_id=message.chat.id, message_ids=d_m_l)
            await message.delete()
        else:
            await message.edit_text("`Lütfen bir kişiyi yanıtlayın.`")
    except Exception as e:
        print(e)
        await message.edit_text(HELP["del"]["deluser"])
        return


@on_msg(pattern="tag")
async def _(client: Client, message: Message):
    try:
        mentions = "@zort"
        leng = 0
        async for x in client.get_chat_members(chat_id=message.chat.id):
            if leng < 4092:
                mentions += f"[\u2063](tg://user?id={x.user.id})"
                leng += 1
        await message.edit_text(mentions)
        await message.delete()
    except Exception:
        await message.edit_text(HELP["del"]["tag"])
        return


@on_msg(pattern="admin")
async def getAdmin(client: Client, message: Message):
    try:
        admins = []
        async for user in client.get_chat_members(
            chat_id=message.chat.id,
            filter=enums.chat_members_filter.ChatMembersFilter.ADMINISTRATORS,
        ):
            admins.append(user.user.mention)
        await client.send_message(chat_id=message.chat.id, text="\n".join(admins))
    except Exception:
        await message.edit_text(HELP["del"]["getadmin"])
        return
