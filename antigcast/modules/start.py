import asyncio

from antigcast import Bot
from pyrogram import filters, enums
from pyrogram.errors import FloodWait
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from antigcast.config import *
from antigcast.helpers.database import *


CTYPE = enums.ChatType

# inline buttons
inlinegc = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="Owner", url="https://t.me/Revans505"),
            InlineKeyboardButton(text="Channel", url="https://t.me/Revanstoreya")
        ]
    ]
)

inline = InlineKeyboardMarkup(
    [
        [
                    InlineKeyboardButton(text="Daftarkan Grup", callback_data = "langganan")
        ],
        [
                    InlineKeyboardButton(text="Creator", url=f"http://t.me/{OWNER_NAME}"),
                    InlineKeyboardButton(text="Channel", url="https://t.me/Revanstoreya")
        ]
    ]
)

def add_panel(username):
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="Tambahkan Ke Group", url=f"http://t.me/{username}?startgroup=appstart")
            ]
        ]
    )

    return button

def admin_panel():
    buttons = [
        [
            InlineKeyboardButton(text="Hubungi Owner", url=f"http://t.me/{OWNER_NAME}")
        ],
    ]

    return buttons

@Bot.on_message(filters.command("start"))
async def start_msgmessag(app : Bot, message : Message):
    bot = await app.get_me()
    username = bot.username
    user = message.from_user.mention
    chat_type = message.chat.type
    if chat_type == CTYPE.PRIVATE:
        msg = f"👋🏻 Hi {user}!\n\nBot ini akan menghapus otomatis pesan gcast yang mengganggu di group. Tambahkan bot sebagai admin agar bisa berjalan dengan baik."
        try:
            await message.reply(text=msg, reply_markup=inline)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply(text=msg, reply_markup=inline)
    elif chat_type in [CTYPE.GROUP, CTYPE.SUPERGROUP]:
        msg = f"**Hey!**\n\n__Jadikan saya sebagai admin group, maka group ini tidak akan ada spam gcast yang mengganggu!__\n\nCreated by {OWNER_NAME}"
        
        try:
            await message.reply(text=msg, reply_markup=inlinegc)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply(text=msg, reply_markup=inlinegc)

@Bot.on_callback_query(filters.regex(r"close"))
async def close_cbq(client: Bot, query: CallbackQuery):
    try:
        await query.message.reply_to_message.delete()
        await client.send_message(query.from_user.id, "**Pendaftaran Dibatalkan**")
    except:
        pass
    try:
        await query.message.delete()
        await client.send_message(query.from_user.id, "**Pendaftaran Dibatalkan**")
    except:
        pass

@Bot.on_callback_query(filters.regex(r"langganan"))
async def bayar_cbq(client: Bot, query: CallbackQuery):
    btn = InlineKeyboardMarkup(admin_panel())
    text = """**Silahkan pilih Plan Subscription untuk berlangganan Bot Anti Gcast Revans**

1 Bulan : `Rp. 50.000,-`
3 Bulan : `RP. 150.000,-`"""
    await query.edit_message_text(
        text = text,
        reply_markup = btn
    )
