from yt_dlp import YoutubeDL
from pyrogram.types import Message, MessageEntity
from pyrogram.enums import message_entity_type
from tauon.core.handler import on_msg
import os
from tauon import HELP
from youtubesearchpython.__future__ import VideosSearch
import asyncio
import re

HELP["vid"] = {
    "vid": ".vid <url> - Video indirir.",
    "yt": ".yt <text> - Youtude'da video arar.",
}


def regexer(text: str) -> list:
    pattern = re.compile(
        "(?:https?\:\/\/)?(?:www\.)?(youtube\.com|youtu\.be)\/([a-zA-Z\?_\-=0-9]*)",
        re.MULTILINE,
    )
    matches = [i.group(0) for i in re.finditer(pattern, text)]
    if matches:
        return matches
    else:
        raise ValueError("No matches found")


async def get_youtube_search_(query: str) -> str:
    videosSearch = VideosSearch(query, limit=10)
    videosResult = await videosSearch.next()
    return "\n".join(
        [
            f"**{i+1}** - [{v['title']}]({v['link']})"
            for i, v in enumerate(videosResult["result"])
        ]
    )


def download_(url):
    ydl_opt = {
        "format": "best[height>=720]/best",
        "outtmpl": "tauon/downloads/%(title)s.%(ext)s",
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
    }
    with YoutubeDL(ydl_opt) as ydl:
        infos = ydl.extract_info(url, download=True)
    return infos.get("title") + "." + infos.get("ext")


@on_msg(pattern="vid (.*)")
async def vid(_, message: Message):
    text = ""
    if message.reply_to_message and message.text.split()[1].isnumeric():
        if message.reply_to_message.entities:
            for entity in message.reply_to_message.entities:
                if entity.type == message_entity_type.MessageEntityType.TEXT_LINK:
                    text += entity.url + " "
                elif entity.type == message_entity_type.MessageEntityType.URL:
                    text += entity.url + " "
            url_list = regexer(text)
            if url_list:
                url = url_list[int(message.text.split()[1]) - 1]
                file_name = download_(url)
                await message.edit("`Indiriliyor...`")
                await message.reply_video(
                    "tauon/downloads/" + file_name, caption=file_name[:-4]
                )
                os.remove("tauon/downloads/" + file_name)
                await message.delete()
            else:
                await message.reply("`Link bulunamadı.`")
                return

        else:
            await message.edit(HELP["vid"]["vid"])
            message.continue_propagation()
            return
    else:
        await message.edit("`Indiriliyor...`")
        file_name = download_(message.text.split(" ")[1])
        await message.reply_video("tauon/downloads/" + file_name, caption=file_name[:-4])
        os.remove("tauon/downloads/" + file_name)
        await message.delete()


@on_msg(pattern="yt (.*)")
async def youtube_search(client, message: Message):
    await message.edit("`Aranıyor...`")
    query = " ".join(message.text.split()[1:])
    text = await get_youtube_search_(query)
    await message.edit(text, disable_web_page_preview=True)
