"""Pesquisa simplificada do Google - @applled"""

import requests

from userge import Message, userge
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@userge.on_cmd(
    "rbg",
    about={
        "header": "Muito pesquisar no RGB",
        "usar": "{tr}goo [pesquisar | responder]",
    },
)
async def rbg_(message: Message):
    """rbg"""
    query = message.input_or_reply_str
    if not query:
        await message.edit("`Vou pesquisar o vento?!`")
        return
    query_encoded = query.replace(" ", "+")
    rar_url = f"https://rarbgprx.org/torrents.php?search={query_encoded}"
    payload = {"format": "json", "url": rar_url}
    r = requests.get("http://is.gd/create.php", params=payload)
    await message.edit(
        f"""
✅ Your **RarBG** search results:
🔗 [{query}]({r.json()['shorturl']})
  ➖➖➖➖
Dev: @iamakima / @twapple
"""
    )
