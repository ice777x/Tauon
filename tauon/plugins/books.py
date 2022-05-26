from pyrogram import Client
from tauon.core.handler import on_msg
from pyrogram.types import Message
from functools import partial
import urllib.request
import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import os


def books(query: str):
    if not os.path.exists("books"):
        os.makedirs("books")
    r = requests.get(
        f"http://libgen.is/search.php?&res=100&req={query}&phrase=1&view=simple&column=def&sort=year&sortmode=DESC"
    )
    soup = BeautifulSoup(r.content, "html.parser")

    book_urls = soup.find_all("a", {"title": "this mirror"})
    r = soup.select("table.c")[0].select("tr td:nth-child(3)")[1:]
    books = [
        {"name": v.find("a").text, "url": book_urls[i]["href"]} for i, v in enumerate(r)
    ]
    return books


async def get_page(session, url):
    async with session.get(url) as response:
        return await response.text()


async def print_response(session, url, book_name):
    html = await get_page(session, url)
    soup2 = BeautifulSoup(html, "html.parser")
    downloads_list = []
    if soup2.select("div#download"):
        dd_ls = [x["href"] for x in soup2.select("div#download ul")[0].select("a")]
        downloads_list.extend(dd_ls)
    else:
        pass
    if downloads_list != []:
        book_down_link = downloads_list[0]
        book_real_name = f'{book_name.strip().replace(" ", "_")}.{book_down_link[::-1].split(".", 1)[0][::-1]}'
        urllib.request.urlretrieve(book_down_link, "books/" + book_real_name)


async def main(query: str) -> None:
    urls = books(query)
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(
            *[
                asyncio.ensure_future(print_response(session, x["url"], x["name"]))
                for x in urls
            ]
        )


@on_msg(pattern="book (.*)")
async def booke(client: Client, message: Message):
    q = " ".join(message.text.split(" ")[1:])
    await main(q)
    list_books = os.listdir("books/")
    tasks = [
        asyncio.ensure_future(client.send_document(message.chat.id, "books/" + i))
        for i in list_books
    ]
    await asyncio.gather(*tasks)
