from shazamio import Shazam

from pyrogram import Client
from pyrogram.types import Message
from tauon import HELP
from tauon.core.handler import on_msg
import os

HELP["shazam"] = {
    "shazam": [
        "shazam - Video veya müzik yanıtlayarak shazam ile şarkıyı bulur.",
        "shazam <q> - Shazam ile şarkı arar.",
    ]
}


async def main(path: str = None, q: str = None):
    shazam = Shazam()
    if q:
        result = await shazam.search_track(q, limit=10)
        return [i["share"]["subject"] for i in result["tracks"]["hits"]]
    if path:
        result = await shazam.recognize_song(path)
        return result["track"]["share"]["subject"]


@on_msg(pattern="shazam ?(.*)")
async def shazam(client: Client, message: Message):
    splitted_txt = message.text.split()
    if len(splitted_txt) > 1:
        await message.edit_text("`Şarkılar aranıyor...`")
        result = await main(q=" ".join(splitted_txt[1:]))
        await message.edit_text(result)
    else:
        if message.reply_to_message:
            if message.reply_to_message.audio:
                await message.edit_text("`Şarkı indiriliyor`")
                file_name = message.reply_to_message.audio.file_name
                await message.reply_to_message.download(
                    file_name="tauon/downloads/" + file_name
                )
                result = await main(path="tauon/downloads/" + file_name)
                if result:
                    await message.edit("`Şarkı bulundu! {}`".format(result))
                    os.remove("tauon/downloads/" + file_name)
                else:
                    await message.edit_text("`Şarkı bulunamadı`")
                    return
            elif message.reply_to_message.video:
                await message.edit("`Video indiriliyor`")
                file_name = message.reply_to_message.video.file_name
                await message.reply_to_message.download(
                    file_name="tauon/downloads/" + file_name
                )
                result = await main(path="tauon/downloads/" + file_name)
                if result:
                    await message.edit_text("`Şarkı bulundu {}`".format(result))
                    os.remove("tauon/downloads/" + file_name)
                else:
                    await message.edit_text("`Videodaki müzik bulunamadı`")
                    return
            else:
                await message.edit_text(HELP["shazam"]["shazam"][0])
                return
