import sys
from pyromod import listen
from pyrogram import Client
from antigcast.config import API_HASH, APP_ID, BOT_TOKEN,LOG_CHANNEL_ID , LOGGER

from antigcast.helpers.database import *


class Bot(Client):
    def __init__(self):
        super().__init__(
            "Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={"root": "antigcast/modules"},
            workers=4,
            bot_token=BOT_TOKEN,
        )
        self.LOGGER = LOGGER

    async def start(self):
        try:
            await super().start()
            usr_bot_me = await self.get_me()
            chats = await get_actived_chats()
            self.username = usr_bot_me.username
            self.namebot = usr_bot_me.first_name
            self.LOGGER(__name__).info(
                f"TG_BOT_TOKEN detected!\n┌ First Name: {self.namebot}\n└ Username: @{self.username}"
            )
        except Exception as a:
            self.LOGGER(__name__).warning(a)
            self.LOGGER(__name__).info(
                "Bot Berhenti."
            )
            sys.exit()

        try:
            db_channel = await self.get_chat(LOG_CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="Bot Actived", disable_notification=True)
            await test.delete()
            self.LOGGER(__name__).info(
                f"LOG_CHANNEL_ID Database detected!\n┌ Title: {db_channel.title}\n└ Chat ID: {db_channel.id}"
            )
        except Exception as e:
            db_channel = await self.get_chat(LOG_CHANNEL_ID)
            self.db_channel = db_channel
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(
                f"Pastikan @{self.username} adalah admin di Channel DataBase anda, LOG_CHANNEL_ID Saat Ini: {db_channel.title}"
            )
            self.LOGGER(__name__).info(
                "Bot Berhenti."
            )
            sys.exit()

app = Bot()