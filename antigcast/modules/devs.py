import sys
import asyncio
import subprocess

from antigcast import Bot
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait

from antigcast.config import *
from antigcast.helpers.tools import *
from antigcast.helpers.database import *


async def send_msg(chat_id, message: Message):
    try:
        if BROADCAST_AS_COPY is False:
            await message.forward(chat_id=chat_id)
        elif BROADCAST_AS_COPY is True:
            await message.copy(chat_id=chat_id)
        return 200, None
    except FloodWait as e:
        await asyncio.sleep(int(e.value))
        return send_msg(chat_id, message)

@Bot.on_message(filters.command("update") & filters.user(OWNER_ID))
async def updatemessag(app : Bot, message : Message):
    xx = await message.reply(f"**Processing Update...**")
    await asyncio.sleep(3)
    try:
        out = subprocess.check_output(["git", "pull"]).decode("UTF-8")
        if "Already up to date." in str(out):
            xnxx =  await xx.edit("**Bot sudah versi Terbaru")
            await asyncio.sleep(3)
            await xnxx.delete()
            return await message.delete()
        await xx.edit(f"```{out}```")
    except Exception as e:
        return await xx.edit(str(e))
    await xx.delete()
    await message.delete()
    await restart()

@Bot.on_message(filters.command("gcast") & filters.user(OWNER_ID))
async def gcast_hndl(app : Bot, message : Message):
    groups = await get_actived_chats()
    msg = get_arg(message)
    if message.reply_to_message:
        msg = message.reply_to_message

    if not msg:
        await message.reply(text="**Reply atau berikan saya sebuah pesan!**")
        return
    
    out = await message.reply(text="**Memulai Broadcast...**")
    
    if not groups:
        await out.edit(text="**Maaf, Broadcast Gagal Karena Belum Ada Grup Yang Terdaftar**")
        return
    
    done = 0
    failed = 0
    for group in groups:
        try:
            await send_msg(group, message=msg)
            done += 1
        except:
            failed += 1
    await out.edit(f"**Berhasil Mengirim Pesan Ke {done} Group.**\n**Gagal Mengirim Pesan Ke {failed} Group.**")