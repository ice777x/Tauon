from pyrogram import Client
from pyrogram.types import Message
from tauon import HELP
from tauon.core.handler import on_msg
import os
from pyrogram.enums.user_status import UserStatus

HELP["user"] = {
    "user": ".user - Yanıtlanan kullanıcının profilini gösterir.",
    "me": ".me - Profilinizi gösterir.",
}


@on_msg(pattern="user")
async def user_(client: Client, message: Message):
    await message.edit_text("`Getting info for us...`")
    if message.reply_to_message:
        from_user = await client.get_users(message.reply_to_message.from_user.id)
        from_chat = await client.get_chat(message.reply_to_message.from_user.id)
    else:
        await message.edit_text("no valid user_id or message specified")
        return

    local_user_photo = await client.download_media(
        message=from_user.photo.big_file_id, file_name="tauon/downloads/user_photo.jpg"
    )
    await message.delete()
    text = f"""<b>USER INFO:</b>

🗣 <b>First Name:</b> <code>{from_user.first_name}</code>
🗣 <b>Last Name:</b> <code>{from_user.last_name}</code>
👤 <b>Username:</b> <code>{from_user.username}</code>
🏢 <b>DC ID:</b> <code>{from_user.dc_id}</code>
🤖 <b>Is Bot:</b> <code>{from_user.is_bot}</code>
🚫 <b>Is Restricted:</b> <code>{from_user.is_restricted}</code>
✅ <b>Is Verified by Telegram:</b> <code>{from_user.is_verified}</code>
🕵️‍♂️ <b>User ID:</b> <code>{from_user.id}</code>
👥 <b>Common Chats:</b> <code>{len(await client.get_common_chats(from_user.id))}</code>
📝 <b>Bio:</b> <code>{from_chat.bio}</code>

👁 <b>Last Seen:</b> <code>{UserStatus(from_user.status).value}</code>
🔗 <b>Permanent Link To Profile:</b> {from_user.mention}"""
    await client.send_photo(
        chat_id=message.chat.id,
        photo=local_user_photo,
        caption=text,
        reply_to_message_id=message.reply_to_message.id
        if message.reply_to_message
        else None,
        disable_notification=True,
    )
    os.remove(local_user_photo)


@on_msg(pattern="me")
async def me_(client: Client, message: Message):
    await message.edit_text("`Getting info for us..`")
    from_user = await client.get_me()
    from_chat = await client.get_chat(message.from_user.id)
    local_user_photo = await client.download_media(
        message=from_user.photo.big_file_id, file_name="tauon/downloads/user_photo.jpg"
    )
    await message.delete()
    text = f"""<b>USER INFO:</b>

🗣 <b>First Name:</b> <code>{from_user.first_name}</code>
🗣 <b>Last Name:</b> <code>{from_user.last_name}</code>
👤 <b>Username:</b> <code>{from_user.username}</code>
🏢 <b>DC ID:</b> <code>{from_user.dc_id}</code>
🤖 <b>Is Bot:</b> <code>{from_user.is_bot}</code>
🚫 <b>Is Restricted:</b> <code>{from_user.is_restricted}</code>
✅ <b>Is Verified by Telegram:</b> <code>{from_user.is_verified}</code>
🕵️‍♂️ <b>User ID:</b> <code>{from_user.id}</code>
👥 <b>Common Chats:</b> <code>{len(await from_user.get_common_chats())}</code>
📝 <b>Bio:</b> <code>{from_chat.bio}</code>

👁 <b>Last Seen:</b> <code>{from_user.status}</code>
🔗 <b>Permanent Link To Profile:</b> {from_user.mention}"""
    await client.send_photo(
        chat_id=message.chat.id,
        photo=local_user_photo,
        caption=text,
        reply_to_message_id=message.reply_to_message.id
        if message.reply_to_message
        else None,
        disable_notification=True,
    )
    os.remove(local_user_photo)
