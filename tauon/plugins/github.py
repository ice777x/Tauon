import requests
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from pyrogram.types import Message

from tauon.core.handler import on_msg
from tauon import HELP

HELP["github"] = {"github": ".github <query> - Github'da arama yapar."}


def git_query(query: str) -> str:
    url = "https://github.com/search?q=" + query
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    try:
        text = "\n".join(
            [
                f'[{i["href"].strip("/")}](https://github.com{i["href"]})'
                for i in soup.select("ul.repo-list")[0].select("a.v-align-middle")
            ]
        )
    except:
        text = f"`{query}` ile alakalı bir şey bulunamadı.."
        return text
    return text


@on_msg(pattern="github (.*)")
async def github_trends(client: Client, message: Message):
    if len(message.text.split()) > 1:
        query = " ".join(message.text.split()[1:])
        await message.edit_text(f"{query} için aranıyor...")
        git_q = git_query(query)
        await message.edit_text(
            f"🧑‍💻**{query} için sonuçlar**\n{git_q}", disable_web_page_preview=True
        )
    else:
        await message.edit_text("Getting Github Trend Topics...")
        url = "https://github.com/trending"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        row = soup.select("article.Box-row")
        try:
            link_name = "\n".join(
                [
                    f'[{i.select("h1 a")[0]["href"].strip("/")}](https://github.com{i.select("h1 a")[0]["href"]}) - {i.select("span.d-inline-block span")[-1].text if len(i.select("span.d-inline-block span")) >1 else ""}'
                    for i in row
                ]
            )
        except Exception as e:
            await message.edit_text(f"`Hata: {e}`")
            return

        try:
            await message.edit_text(
                f"**Github Trend**\n{link_name}", disable_web_page_preview=True
            )
        except Exception as e:
            await message.edit_text(f"`Hata: {e}`")
            return
