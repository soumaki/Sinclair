""" Configuração para o modo ausente - Adaptado por #NoteX/Samuca/Applled / AppleBot"""

import asyncio
import random
import time
from random import randint
from re import compile as comp_regex

from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from userge import Config, Message, filters, get_collection, userge
from userge.plugins.utils.afk_inline import (
    _send_inline_afk_,
    send_inline_afk,
    send_inline_afk_,
)
from userge.utils import time_formatter

_TELE_REGEX = comp_regex(
    r"http[s]?://(i\.imgur\.com|telegra\.ph/file|t\.me)/(\w+)(?:\.|/)(gif|mp4|jpg|png|jpeg|[0-9]+)(?:/([0-9]+))?"
)

CHANNEL = userge.getCLogger(__name__)
SAVED_SETTINGS = get_collection("CONFIGS")
AFK_COLLECTION = get_collection("AFK")

IS_AFK = False
IS_AFK_FILTER = filters.create(lambda _, __, ___: bool(IS_AFK))
REASON = ""
TIME = 0.0
USERS = {}


async def _init() -> None:
    global IS_AFK, REASON, TIME  # pylint: disable=global-statement
    data = await SAVED_SETTINGS.find_one({"_id": "AFK"})
    if data:
        IS_AFK = data["on"]
        REASON = data["data"]
        TIME = data["time"] if "time" in data else 0
    async for _user in AFK_COLLECTION.find():
        USERS.update({_user["_id"]: [_user["pcount"], _user["gcount"], _user["men"]]})


@userge.on_cmd(
    "afk",
    about={
        "header": "Definir status para modo ausente",
        "descrição": "Este modo vai informar sua ausência e respondará à todos que te mencionarem. \n"
        "Informará o motivo e o tempo de ausência.",
        "Como usar": "{tr}afk ou {tr}afk [motivo] | endereço.com/arquivo.gif|mp4|jpg",
    },
    allow_channels=False,
)
async def ausente(message: Message) -> None:
    """Modo ausente ligado/desligado"""
    global REASON, IS_AFK, TIME  # pylint: disable=global-statement
    IS_AFK = True
    TIME = time.time()
    REASON = message.input_str
    match_ = _TELE_REGEX.search(REASON)
    if match_:
        r_ = REASON.split(" | ", maxsplit=1)
        STATUS_ = r_[0]
        await asyncio.gather(
            CHANNEL.log(f"Sumindo! : `{STATUS_}` [\u200c]({match_.group(0)})"),
            message.edit("`Fui!`", del_in=1),
            AFK_COLLECTION.drop(),
            SAVED_SETTINGS.update_one(
                {"_id": "AFK"},
                {"$set": {"on": True, "data": STATUS_, "time": TIME}},
                upsert=True,
            ),
        )
    else:
        await asyncio.gather(
            CHANNEL.log(f"Sumindo!  `{REASON}`"),
            message.edit("`Fuii!`", del_in=1),
            AFK_COLLECTION.drop(),
            SAVED_SETTINGS.update_one(
                {"_id": "AFK"},
                {"set": {"on": True, "data": REASON, "time": TIME}},
                upsert=True,
            ),
        )


@userge.on_filters(
    IS_AFK_FILTER
    & ~filters.me
    & ~filters.bot
    & ~filters.user(Config.TG_IDS)
    & ~filters.edited
    & (
        filters.mentioned
        | (
            filters.private
            & ~filters.service
            & (
                filters.create(lambda _, __, ___: Config.ALLOW_ALL_PMS)
                | Config.ALLOWED_CHATS
            )
        )
    ),
    allow_via_bot=False,
)
async def respostas(message: Message) -> None:
    """Configurações das mensagens automáticas"""
    if not message.from_user:
        return
    user_id = message.from_user.id
    chat = message.chat
    user_dict = await message.client.get_user_dict(user_id)
    time_formatter(round(time.time() - TIME))
    coro_list = []
    if user_id in USERS:
        if not (USERS[user_id][0] + USERS[user_id][1]) % randint(2, 4):
            match = _TELE_REGEX.search(REASON)
            if match:
                link = (
                    match.group(0)
                    if match.group(3) != "mp4"
                    else str(match.group(0)).replace("mp4", "gif")
                )
                type_, media_ = await _afk_.check_media_link(link)
                if type_ == "url_gif":
                    await send_inline_afk(message)
                if type_ == "url_image":
                    await send_inline_afk_(message)
            else:
                await _send_inline_afk_(message)
        if chat.type == "private":
            USERS[user_id][0] += 1
        else:
            USERS[user_id][1] += 1
    else:
        match = _TELE_REGEX.search(REASON)
        if match:
            link = (
                match.group(0)
                if match.group(3) != "mp4"
                else str(match.group(0)).replace("mp4", "gif")
            )
            type_, media_ = await _afk_.check_media_link(link)
            if type_ == "url_image":
                await send_inline_afk_(message)
            elif type_ == "url_gif":
                await send_inline_afk(message)
        else:
            await _send_inline_afk_(message)
        if chat.type == "private":
            USERS[user_id] = [1, 0, user_dict["mention"]]
        else:
            USERS[user_id] = [0, 1, user_dict["mention"]]
    if chat.type == "private":
        coro_list.append(
            CHANNEL.log(
                f"𝙴𝚗𝚚𝚞𝚊𝚗𝚝𝚘 𝚎𝚜𝚝𝚊𝚟𝚊 𝚊𝚞𝚜𝚎𝚗𝚝𝚎 | #PRIVADO\n"
                f"**Chegou Uma Nova Mensagem Privada**\n"
                f"𝙴𝚗𝚟𝚒𝚊𝚍𝚊 𝚙𝚘𝚛:\n"
                f"🏷 | {user_dict['mention']}\n"
                f"➖➖➖➖\n"
                f"💬 **MENSAGEM ORIGINAL:**\n"
                f" ╰• __{message.text}__"
            )
        )
    else:
        coro_list.append(
            CHANNEL.log(
                "#GRUPO\n"
                f"🍏 AFK Log | **AppleBot**\n"
                f"Alguém #Mencionou Você\n"
                f"➖➖➖➖➖➖\n"
                f"<b>🏷 Enviada por:</b> {user_dict['mention']}\n"
                f"<b> ╰• No Grupo:</b> [{chat.title}](http://t.me/{chat.username})\n"
                f"<b>🔗 [Link da Mensagem](https://t.me/c/{str(chat.id)[4:]}/{message.message_id})\n"
                f"➖➖➖➖➖➖\n"
                f"💬 __{message.text}__\n\n"
            )
        )
    coro_list.append(
        AFK_COLLECTION.update_one(
            {"_id": user_id},
            {
                "$set": {
                    "pcount": USERS[user_id][0],
                    "gcount": USERS[user_id][1],
                    "men": USERS[user_id][2],
                }
            },
            upsert=True,
        )
    )
    await asyncio.gather(*coro_list)


class _afk_:
    def out_str() -> str:
        _afk_time = time_formatter(round(time.time() - TIME))
        _r = REASON.split(" | ", maxsplit=1)
        _STATUS = _r[0]
        out_str = (
            f""
            f""
        )
        return out_str

    def _out_str() -> str:
        afk_time_ = time_formatter(round(time.time() - TIME))
        out_str = (
            f""
            f""
        )
        return out_str

    def link() -> str:
        _match_ = _TELE_REGEX.search(REASON)
        if _match_:
            link = _match_.group(0)
            return link

    async def check_media_link(media_link: str):
        match_ = _TELE_REGEX.search(media_link.strip())
        if not match_:
            return None, None
        if match_.group(1) == "i.imgur.com":
            link = match_.group(0)
            link_type = "url_gif" if match_.group(3) == "gif" else "url_image"
        elif match_.group(1) == "telegra.ph/file":
            link = match_.group(0)
            link_type = "url_gif" if match_.group(3) == "gif" else "url_image"
        else:
            link_type = "tg_media"
            if match_.group(2) == "c":
                chat_id = int("-100" + str(match_.group(3)))
                message_id = match_.group(4)
            else:
                chat_id = match_.group(2)
                message_id = match_.group(3)
            link = [chat_id, int(message_id)]
        return link_type, link

    def afk_buttons() -> InlineKeyboardMarkup:
        buttons = [
[InlineKeyboardButton(text="✅ STATUS", callback_data="status_afk"),
             InlineKeyboardButton(text="⭕️ FM", url="https://t.me/MakiFMBot"),
             InlineKeyboardButton(text="👾", url=Config.BIO_STT),],]
        return InlineKeyboardMarkup(buttons)

@userge.on_filters(IS_AFK_FILTER & filters.outgoing, group=-1, allow_via_bot=False)
async def logs(message: Message) -> None:
    """Detalhes - Log do Modo Ausente"""
    global IS_AFK  # pylint: disable=global-statement
    IS_AFK = False
    afk_time = time_formatter(round(time.time() - TIME))
    replied: Message = await message.reply("`Não estou mais ausente!`", log=__name__)
    coro_list = []
    if USERS:
        p_msg = ""
        g_msg = ""
        p_count = 0
        g_count = 0
        for pcount, gcount, men in USERS.values():
            if pcount:
                p_msg += f"👤 {men} ✉️ **{pcount}**\n"
                p_count += pcount
            if gcount:
                g_msg += f"👥 {men} ✉️ **{gcount}**\n"
                g_count += gcount
        coro_list.append(
            replied.edit(
                f"`💬 Na sua Inbox: {p_count + g_count} mensagens. "
                f"▫️ Confira os detalhes no log.`\n\n💤 **Ausente por** : __{afk_time}__",
                del_in=1,
            )
        )
        out_str = (
            f"📂 𝙼𝚎𝚗𝚜𝚊𝚐𝚎𝚗𝚜 𝚗𝚊 𝙸𝚗𝚋𝚘𝚡: **{p_count + g_count}** \n▫️ Em contato: **{len(USERS)}** desgraçado(s) "
            + f"\n▫️ **Ausente por** : __{afk_time}__\n\n"
        )
        if p_count:
            out_str += f"\n{p_count} 𝙼𝙴𝙽𝚂𝙰𝙶𝙴𝙽𝚂 𝙿𝚁𝙸𝚅𝙰𝙳𝙰𝚂:\n{p_msg}"
        if g_count:
            out_str += f"\n{g_count} 𝙼𝙴𝙽𝚂𝙰𝙶𝙴𝙽𝚂 𝙴𝙼 𝙶𝚁𝚄𝙿𝙾𝚂:\n{g_msg}"
        coro_list.append(CHANNEL.log(out_str))
        USERS.clear()
    else:
        await asyncio.sleep(3)
        coro_list.append(replied.delete())
    coro_list.append(
        asyncio.gather(
            AFK_COLLECTION.drop(),
            SAVED_SETTINGS.update_one(
                {"_id": "AFK"}, {"$set": {"on": False}}, upsert=True
            ),
        )
    )
    await asyncio.gather(*coro_list)

    # # # teste # # #
    @userge.bot.on_callback_query(filters.regex(pattern=r"^status_afk$"))
    async def status_afk_(_, c_q: CallbackQuery):
        c_q.from_user.id
        await c_q.answer(
            f"👾 @iamakima 𝐒𝐓𝐀𝐓𝐔𝐒:\n\n𝐏𝐨𝐬𝐬í𝐯𝐞𝐢𝐬 𝐌𝐨𝐭𝐢𝐯𝐨𝐬:\n ╰• {random.choice(MOTIVOS)}\n\n🔗 𝐁𝐢𝐨: @biorange",
            show_alert=True,
        )
        return status_afk_

    @userge.bot.on_callback_query(filters.regex(pattern=r"^status_apple$"))
    async def _status_afk(_, c_q: CallbackQuery):
        c_q.from_user.id
        await c_q.answer(
            f"🍎 @applled 𝐁𝐈𝐎/Projects:\nТак вам любопытно\n\nHi, human!\n{random.choice(BIO_AFK)}\n\n🔗 𝐁𝐢𝐨: @biorange",
            show_alert=True,
        )
        return _status_afk


MOTIVOS = (
    "Curioso, né? Não estou, jovem.",
    "Te respondo assim que eu ficar onlime, combinado?",
    "Meu celular descarregou. Será?",
    "Paciência, volto logo.",
    "Você pode usar o Google, sabia disso?",
    "Ainda não sei o que tu quer, mas tentou pesquisar?",
    "Cliclou aqui, quanta curiosidade...",
    "Esse Less. é o meu blog pessoal no TG ;)",
    "Leia minha bio em @biorange.",
    "Zzzz...",
    "Sem motivo, eu só quis sumir.",
    "Posso estar trabalhando...",
    "Já bebeu água hoje? Vá beber do mesmo jeito. Não estou.",
    "Posso ter saído ou simplesmente estou assistindo agora.",
    "Não estou, não tá vendo?",
    "Estou em algum lugar, menos aqui.",
    "Não cansa?",
    "Queria mesmo era chocolate, mas chocolate branco. Vai me dar?",
    "AUTO REPLY fofo(a)!",
    "Qual parte do AFK tu não entendeu?",
    "NÃO ESTOU!",
    "Netflix!",
    "Disney+",
    "No Spotify...",
    "Voltarei assim que possível.",
    "Deixe seu recado, peste.",
    "Zzzz...?",
    "Dê um tempo...",

)

BIO_AFK = (
    "𝐂𝐇𝐄𝐂𝐊 𝐓𝐇𝐈𝐒:\n\n𝐋𝐢𝐤𝐞 𝐓𝐰𝐞𝐞𝐭𝐬\n🔗 -- \n𝐁𝐢𝐨\n🔗 -- \n ╰• 𝘔𝘰𝘳𝘦 𝘤𝘰𝘮𝘪𝘯𝘨 𝘴𝘰𝘰𝘯...",
)
AFK_REASONS = ("𝙸 𝚌𝚊𝚗'𝚝 𝚝𝚊𝚕𝚔 𝚛𝚒𝚐𝚑𝚝 𝚗𝚘𝚠.",)
