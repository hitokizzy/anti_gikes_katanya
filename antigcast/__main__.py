import asyncio
from antigcast import Bot, app
from antigcast.config import LOGGER, LOG_CHANNEL_ID
from pyrogram import idle
from antigcast.helpers.tools import checkExpired


loop = asyncio.get_event_loop_policy().get_event_loop()

async def main():
    try:
        await app.start()
        app.me = await app.get_me()
        username = app.me.username
        namebot = app.me.first_name
        log = await app.send_message(LOG_CHANNEL_ID, "BOT AKTIF!")
        LOGGER("INFO").info(f"{namebot} | [ @{username} ] | 🔥 BERHASIL DIAKTIFKAN! 🔥")
        await log.delete()
    except Exception as a:
        print(a)
    LOGGER("INFO").info(f"[🔥 BOT AKTIF! 🔥]")
    await checkExpired()
    await idle()


LOGGER("INFO").info("Starting Bot...")
loop.run_until_complete(main())