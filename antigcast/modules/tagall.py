import random
from asyncio import sleep

import asyncio

from antigcast import Bot
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait, UserNotParticipant

from antigcast.config import *
from antigcast.helpers.tools import *
from antigcast.helpers.admins import *
from antigcast.helpers.message import *
from antigcast.helpers.database import *

STATUS = enums.ChatMemberStatus
spam_chats = []
emoji = "😀 😃 😄 😁 😆 😅 😂 🤣 😭 😗 😙 😚 😘 🥰 😍 🤩 🥳 🤗 🙃 🙂 ☺️ 😊 😏 😌 😉 🤭 😶 😐 😑 😔 😋 😛 😝 😜 🤪 🤔 🤨 🧐 🙄 😒 😤 😠 🤬 ☹️ 🙁 😕 😟 🥺 😳 😬 🤐 🤫 😰 😨 😧 😦 😮 😯 😲 😱 🤯 😢 😥 😓 😞 😖 😣 😩 😫 🤤 🥱 😴 😪 🌛 🌜 🌚 🌝 🎲 🧩 ♟ 🎯 🎳 🎭💕 💞 💓 💗 💖 ❤️‍🔥 💔 🤎 🤍 🖤 ❤️ 🧡 💛 💚 💙 💜 💘 💝 🐵 🦁 🐯 🐱 🐶 🐺 🐻 🐨 🐼 🐹 🐭 🐰 🦊 🦝 🐮 🐷 🐽 🐗 🦓 🦄 🐴 🐸 🐲 🦎 🐉 🦖 🦕 🐢 🐊 🐍 🐁 🐀 🐇 🐈 🐩 🐕 🦮 🐕‍🦺 🐅 🐆 🐎 🐖 🐄 🐂 🐃 🐏 🐑 🐐 🦌 🦙 🦥 🦘 🐘 🦏 🦛 🦒 🐒 🦍 🦧 🐪 🐫 🐿️ 🦨 🦡 🦔 🦦 🦇 🐓 🐔 🐣 🐤 🐥 🐦 🦉 🦅 🦜 🕊️ 🦢 🦩 🦚 🦃 🦆 🐧 🦈 🐬 🐋 🐳 🐟 🐠 🐡 🦐 🦞 🦀 🦑 🐙 🦪 🦂 🕷️ 🦋 🐞 🐝 🦟 🦗 🐜 🐌 🐚 🕸️ 🐛 🐾 🌞 🤢 🤮 🤧 🤒 🍓 🍒 🍎 🍉 🍑 🍊 🥭 🍍 🍌 🌶 🍇 🥝 🍐 🍏 🍈 🍋 🍄 🥕 🍠 🧅 🌽 🥦 🥒 🥬 🥑 🥯 🥖 🥐 🍞 🥜 🌰 🥔 🧄 🍆 🧇 🥞 🥚 🧀 🥓 🥩 🍗 🍖 🥙 🌯 🌮 🍕 🍟 🥨 🥪 🌭 🍔 🧆 🥘 🍝 🥫 🥣 🥗 🍲 🍛 🍜 🍢 🥟 🍱 🍚 🥡 🍤 🍣 🦞 🦪 🍘 🍡 🥠 🥮 🍧 🍨".split(
    " "
)

def get_arg(message: Message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])

async def isAdmin(filter, client, update):
    try:
        member = await client.get_chat_member(chat_id=update.chat.id, user_id=update.from_user.id)
    except FloodWait as wait_err:
        await sleep(wait_err.value)
    except UserNotParticipant:
        return False
    except:
        return False

    return member.status in [STATUS.OWNER, STATUS.ADMINISTRATOR]

Admin = filters.create(isAdmin)

@Bot.on_message(filters.command("tagall") & filters.group & Admin)
async def tagall(client, message: Message):
    await message.delete()
    chat_id = message.chat.id
    args = get_arg(message)
    if not args:
        args = "Hi!"
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    m = client.get_chat_members(chat_id)
    async for usr in m:
        if not chat_id in spam_chats:
            break
        usrnum += 1
        usrtxt += f"[{random.choice(emoji)}](tg://user?id={usr.user.id}) "
        if usrnum == 5:
            txt = f"**{args}**\n\n{usrtxt}"
            try:
                await client.send_message(chat_id, txt)
            except FloodWait as e:
                await sleep(e.value)
                await client.send_message(chat_id, txt)

            await sleep(2)
            usrnum = 0
            usrtxt = ""
    try:
        await client.send_message(chat_id, "**Proses Tag All selesai.")
        spam_chats.remove(chat_id)
    except:
        pass

@Bot.on_message(filters.command("cancel") & filters.group & Admin)
async def untag(client, message: Message):
    if not message.chat.id in spam_chats:
        return await message.reply("**Sepertinya tidak ada tagall disini.**")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.reply("**Proses Tag All berhenti..**")