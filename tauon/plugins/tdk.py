from tauon.core.handler import on_msg
from pyrogram.types import Message
import requests
from tauon import HELP

HELP["tdk"] = {"tdk": ".tdk <kelime> - Türkçe'de kelimenin anlamını gösterir."}


def anlam(kelime: str):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
    }
    r = requests.get("https://sozluk.gov.tr/gts?ara=" + kelime, headers=headers)
    res = r.json()[0]
    anlamlist = res["anlamlarListe"]
    text = f"{kelime.capitalize()}\n"
    text += "\n".join(["- " + i["anlam"] for i in anlamlist])
    return text


@on_msg(pattern="tdk")
async def tdk_(_, message: Message):
    try:
        mesaj = " ".join(message.text.split()[1:]).strip()
    except IndexError:
        await message.edit_text(HELP["tdk"]["tdk"])
        return
    text = anlam(mesaj)
    await message.edit_text(text)
