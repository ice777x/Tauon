from tauon import HELP
from tauon.core.handler import on_msg
from pyrogram.types import Message
from pyrogram import Client
from tauon.modules import tag
import asyncio
import os

HELP["tools"] = {
    "plugins": [
        ".p install - bir plugin dosyası yanıtlayarak plugin yüklemenizi sağlar",
        ".p uninstall - bir plugin adı girerek veya plugin dosyasını yanıtlayarak plugin kaldırmanızı sağlar.",
    ]
}


@on_msg(pattern="(p|plugins?) ?(.*)")
async def plugin(_, message: Message):
    plugins = os.listdir("tauon/plugins")
    if len(message.text.split()) > 1:
        if "install" in message.text:
            if message.reply_to_message and message.reply_to_message.document:
                if message.reply_to_message.document.file_name in plugins:
                    os.remove(
                        "tauon/plugins/" + message.reply_to_message.document.file_name
                    )
                    await message.reply_to_message.download(
                        "tauon/plugins/" + message.reply_to_message.document.file_name
                    )
                    await message.edit("`Plugin yüklendi.`")
                else:
                    if "@TauonPlugin" in message.reply_to_message.caption:
                        await message.edit_text("`Plugin yükleniyor...`")
                        await message.reply_to_message.download(
                            "tauon/plugins/"
                            + message.reply_to_message.document.file_name,
                        )
                        await message.edit_text("`Plugin yüklendi!`")
            else:
                await message.edit("@TauonPlugin harici bir plugin yükleyemezsin.")
        elif "uninstall" in message.text:
            if message.reply_to_message and message.reply_to_message.document:
                await message.edit_text("`Plugin kaldırılıyor...`")
                if "@TauonPlugin" in message.reply_to_message.caption:
                    file_name = message.reply_to_message.document.file_name
                    try:
                        os.remove("tauon/plugins/" + file_name)
                    except:
                        await message.edit(
                            "`Plugin bulunamadı mevcut pluginler\n{}`".format(
                                ", ".join([i[:-3] for i in plugins if i[-3:] == ".py"])
                            )
                        )
                else:
                    s_plugin = "".join(message.text.split(" ")[2:]) + ".py"
                    if s_plugin in plugins:
                        os.remove("tauon/plugins/" + s_plugin)
                        await message.edit_text("`Plugin kaldırıldı!`")
                    os.remove(
                        "tauon/plugins/" + message.reply_to_message.document.file_name
                    )
                    await message.edit_text("`Plugin yüklendi!`")
            else:
                await message.edit("@TauonPlugin harici bir plugin yükleyemezsin.")
        else:
            HELP["tools"]["plugins"]

    else:
        tx_plugin = ", ".join([i[:-3] for i in plugins if i[-3:] == ".py"])
        await message.edit(f"`Mevcut pluginler:\n{tx_plugin}`")


@on_msg(pattern="tagall ?")
async def tagall(client: Client, message: Message):
    t = tag.Tagger(client=client,offset=0,channel="@goygoy_muhabbet_sohbet")
    users = await t.tag_all()
    ids = [i.id for i in users]
    ###########################
    nw_users = []
    first = 0
    l_i = 200
    while first <= len(ids):
        users2 = await client.get_users(ids[first:l_i])
        nw_users.extend(users2)
        first += 200
        l_i += 200
    a = "\n".join(
        [
            f"[{i.username}](tg://user?id={i.id})"
            if i.username
            else f"[{i.first_name}](tg://user?id={i.id})"
            for i in nw_users
        ]
    )
    with open('tagged.txt',"w",encoding='utf-8') as file:
        file.write(a)


@on_msg(pattern="sendpy (.*)")
async def send_py(client: Client,message: Message):
    plugins = [i for i in os.listdir('tauon/plugins') if i.endswith(".py")]
    text = message.text.split()[1]
    if text.endswith(".py"):
        if text in plugins:
            await client.send_document(message.chat.id,f"tauon/plugins/{text}")
        else:
            await message.edit("`Yüklü Plugin bulunamadı!`")
            return
    else:
        if message.text.split()[1]+".py" in plugins:
            await client.send_document(message.chat.id,f"tauon/plugins/{message.text.split()[1]+'.py'}")
        
        else:
            await message.edit("`Yüklü Plugin bulunamadı!`")
            return