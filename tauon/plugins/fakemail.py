import requests
from pyrogram.types import Message
from tauon import HELP
from tauon.core.handler import on_msg

HELP["fakemail"] = {"fakemail": ".fakemail - Fakemail alır."}


def get_mail():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    }
    r = requests.get(
        "https://tempail.com/tr/fake-mail/",
        headers=headers,
    )
    return r.text.split('class="adres-input" value="')[1].split('"')[0]


@on_msg(pattern="fakemail")
async def fake_mail(_, message: Message):
    await message.edit_text("...")
    try:
        text = get_mail()
        await message.edit_text(f"**Fake mail:** `{text}`")
    except Exception as e:
        try:
            text = get_mail()
            await message.edit_text(f"**Fake mail:** `{text}`")
            return
        except Exception as e:
            await message.edit_text(f"`{e}`")
            return
