# @Laranjudo - Lindo e maravilhoso #
""" Módulo retrabalhado para o Modo Ausente com escolhas aleatórias"""
import asyncio
import random
from userge import Message, userge

# Motivos 

STATUS = (
    "Posso ter saído ou simplesmente estou assistindo agora.",
    "Não estou, não tá vendo?",
    "Estou em algum lugar, menos aqui.",
    "Não cansa?",
    "Queria mesmo era chocolate, mas chocolate branco. Vai me dar?",
    "AUTO REPLY fofo(a)!",
    "Qual parte do AFK tu não entendeu?",
    "NÃO ESTOU!",
)

# Ações - Media dos Motivos 
STATUSM = (
    "https://telegra.ph/file/6ca775f686db817235437.gif",
    "https://telegra.ph/file/1ae2b317b1ced5e16c47f.gif",
    "https://telegra.ph/file/6ca775f686db817235437.gif",
)

@userge.on_cmd(
    "status",
    about={
        "header": "Modo Ausente já definido os status/medias",
        "flags": {
            "-on": "Modo Ausente: Ligado...",
            "-fui": "Modo Ausente: Ligado...",
        },
        "como usar": "{tr}status -flag",
        "exemplo": "{tr}status-on",
    },
    del_pre=True,
    allow_channels=False,
)

async def escolhas_ausente(message: Message):
    """ Motivos para o Modo Ausente """
    await message.edit("`𝙴𝚗𝚝𝚎𝚗𝚍𝚒, 𝙼𝚎𝚜𝚝𝚛𝚎. 𝙰𝚐𝚞𝚊𝚛𝚍𝚎... 𝙼𝚘𝚍𝚘 𝙰𝚞𝚜𝚎𝚗𝚝𝚎 𝚙𝚛é-𝚍𝚎𝚏𝚒𝚗𝚒𝚍𝚘 𝚊𝚝𝚒𝚟𝚊𝚍𝚘 ✅`", log=__name__)
    if "on" in message.flags:
            await message.edit(
                f"!afk {random.choice(STATUS)} | {random.choice(STATUSM)}",
                del_in=1,
            )
    if "fui" in message.flags:
            await message.edit(
                f"!afk {random.choice(STATUS)} | {random.choice(STATUSM)}",
                del_in=1,
            )
