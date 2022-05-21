from pyrogram.types import Message
from tauon import HELP
from tauon.core.handler import on_msg
import requests


HELP["cevir"] = {"cevir": ".cevir <text> | .cevir"}


def cevir_f(cevirilecek):
    """
    if cek["result"] == "success":
        await message.edit_text(cek["translated_text"])

    elif cek["result"] == "error":
        await message.edit_text("`Üzgünüm çeviremedim`")
    else:
        pass
    """
    data1 = {
        "detect_new_text": 0,
        "rtk_priv": "none",
        "rtk_p": "%7B%7D",
        "_gat_gtag_UA_3411294_31": 1,
        "text_to_translate": cevirilecek,
    }

    abc = requests.post(
        "https://www.translate.com/translator/ajax_lang_auto_detect", data=data1
    ).json()

    lang = abc["language"]
    url = "https://www.translate.com/translator/ajax_translate"
    if lang == "tr":
        cevir = requests.post(
            url,
            data={
                "text_to_translate": cevirilecek,
                "source_lang": lang,
                "translated_lang": "en",
            },
        )

    else:
        cevir = requests.post(
            url,
            data={
                "text_to_translate": cevirilecek,
                "source_lang": lang,
                "translated_lang": "tr",
            },
        )

    cek = cevir.json()
    return cek


@on_msg(pattern="cevir ?(.*)")
async def cevir(_, message: Message):
    try:
        await message.edit_text("`Çeviriliyor..`")
        if not message.reply_to_message:
            cevirilecek = message.text.split(".cevir ")[1]
        else:
            cevirilecek = message.reply_to_message.text
        cek = cevir_f(cevirilecek)
        if cek["result"] == "success":
            await message.edit_text(cek["translated_text"])

        elif cek["result"] == "error":
            await message.edit_text("`Üzgünüm çeviremedim`")
        else:
            pass
    except Exception:
        await message.edit_text(HELP["cevir"]["cevir"])
        return
