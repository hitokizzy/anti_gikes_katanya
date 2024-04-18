import asyncio
import datetime

from pytz import timezone
from dateutil.relativedelta import relativedelta

from antigcast import Bot
from pyrogram import filters
from pyrogram.types import Message

from antigcast.config import *
from antigcast.helpers.tools import *
from antigcast.helpers.database import *


@Bot.on_message(filters.command("addgc") & filters.user(OWNER_ID))
async def addgcmessag(app : Bot, message : Message):
    chat_id = message.chat.id
    chat_name = message.chat.title
    hari = get_arg(message)
    if not hari:
        hari = "30"
    xxnx = await message.reply(f"`Menambahakan izin dalam grup ini..`")
    now = datetime.datetime.now(timezone("Asia/Jakarta"))
    expired = now + relativedelta(days=int(hari))
    expired_date = expired.strftime("%d-%m-%Y")
    chats = await get_actived_chats()
    if chat_id in chats:
        msg = await message.reply("Maaf, Group ini sudah di izinkan untuk menggunakan Bot.")
        await asyncio.sleep(10)
        await msg.delete()
        return
    
    try:
        added = await add_actived_chat(chat_id)
        if added:
            await set_expired_date(chat_id, expired)
    except BaseException as e:
        print(e)

    await xxnx.edit(f"**BOT AKTIF**\nGroup : `{chat_name}`\nExp : `{expired_date}` | `{hari} Hari..`")
    await asyncio.sleep(10)

@Bot.on_message(filters.command("add") & filters.user(OWNER_ID))
async def addgroupmessag(app : Bot, message : Message):
    xxnx = await message.reply(f"`Menambahakan izin dalam grup ini..`")
    if len(message.command) > 3:
        return await xxnx.edit(f"**Gunakan Format** : `/add group_id hari`")
    command, group, hari = message.command[:3]
    chat_id = int(group)
    now = datetime.datetime.now(timezone("Asia/Jakarta"))
    expired = now + relativedelta(days=int(hari))
    expired_date = expired.strftime("%d-%m-%Y")
    chats = await get_actived_chats()
    if chat_id in chats:
        msg = await message.reply("Maaf, Group ini sudah di izinkan untuk menggunakan Bot.")
        await asyncio.sleep(10)
        await msg.delete()
        return
    
    try:
        added = await add_actived_chat(chat_id)
        if added:
            await set_expired_date(chat_id, expired)
    except BaseException as e:
        print(e)

    await xxnx.edit(f"**BOT AKTIF**\nGroup ID: `{group}`\nExp : `{expired_date}` | `{hari} Hari..`")
    await asyncio.sleep(10)
    await xxnx.delete()
    await message.delete()

@Bot.on_message(filters.command("rmgc") & filters.user(OWNER_ID))
async def remgcmessag(app : Bot, message : Message):
    chat_id = int(get_arg(message))

    if not chat_id:
        chat_id = message.chat.id
        
    xxnx = await message.reply(f"`Menghapus izin dalam grup ini..`")
    try:
        await rem_actived_chat(chat_id)
        await rem_expired_date(chat_id)
    except BaseException as e:
        print(e)

    await xxnx.edit(f"Removed `{chat_id}` | Group ini tidak di izinkan untuk mengunakan Bot..`")
    await asyncio.sleep(10)
    await xxnx.delete()
    await message.delete()

@Bot.on_message(filters.command("groups") & filters.user(OWNER_ID))
async def get_groupsmessag(app : Bot, message : Message):
    group = []
    chats = await get_actived_chats()
    for chat in chats:
        group.append(chat)
    if not group:
        return await message.reply("**Belum Ada Group yang Terdaftar.**")
    # group.sort()
    resp = await message.reply("**Memuat database...")
    msg = f"**Daftar Group Aktif**\n\n"
    num = 0
    for gc in group:
        expired = await get_expired_date(int(gc))
        if not expired:
            expired_date = "None"
        else:
            expired_date = expired.strftime("%d-%m-%Y")
        try:
            get = await app.get_chat(int(gc))
            gname = get.title
            glink = get.invite_link
            gid = get.id
            num += 1
            msg += f"**{num}. {gname}**\n├ Group ID : `{gid}`\n├ Link : [Tap Here]({glink})\n└ Expired : `{expired_date}`\n\n"
        except:
            msg += f"**{num}. {gc}**\n└ Expired : `{expired_date}`\n\n"

    await resp.edit(msg, disable_web_page_preview=True)