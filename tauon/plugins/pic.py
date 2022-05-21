import requests
from bs4 import BeautifulSoup
from tauon import HELP
from tauon.core.handler import on_msg
from pyrogram.types import Message
from pyrogram import Client
import asyncio


def get_yandex_photo(query: str, n: int) -> list:
    url: str = "https://yandex.com.tr/gorsel/search?p=1&text=" + query
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    resim_list = ["https:" + i["src"] for i in soup.select("img.serp-item__thumb")]
    return resim_list[:n]


@on_msg(pattern="pic (.*)")
async def yandex_photo(client: Client, message: Message):
    await message.delete()
    split_text = message.text.split()
    if split_text[1].isnumeric():
        n = int(split_text[1])
    else:
        n = 5
    q = " ".join(split_text[2:])
    try:
        get_photos = get_yandex_photo(q, n)
        chat_id = message.chat.id
        task = [
            asyncio.create_task(client.send_photo(chat_id, url)) for url in get_photos
        ]
        await asyncio.gather(*task)
    except Exception as e:
        await message.reply_text(str(e))
        return
