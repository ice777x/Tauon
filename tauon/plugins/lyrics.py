import requests
from pyrogram.types import Message
from tauon.core.handler import on_msg
from tauon import HELP

HELP['lyrics'] = {'lyrics': '.lyrics <song_name>'}

@on_msg(pattern='lyrics ?(.*)')
async def lyrics(_, message: Message):
    query = " ".join(message.text.split()[1:])
    await message.edit(f"**{query}** `için şarkı sözleri aranıyor...`")
    r = requests.get("https://apiice.herokuapp.com/lyrics/?query="+query)
    data = r.json()
    if data['status_code'] == 200 and data['response'] != []:
        await message.edit_text(data['response'][0]['lyrics'])
    else:
        await message.edit_text(f"**{query}** `için şarkı sözleri bulunamadı`")