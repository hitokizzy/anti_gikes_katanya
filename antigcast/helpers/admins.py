import asyncio
from pyrogram import filters, enums
from pyrogram.errors.exceptions.flood_420 import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant

STATUS = enums.ChatMemberStatus

async def isMember(filter, client, update):
    try:
        member = await client.get_chat_member(chat_id=update.chat.id, user_id=update.from_user.id)
    except FloodWait as wait_err:
        await asyncio.sleep(wait_err.value)
    except UserNotParticipant:
        return False
    except:
        return False

    return member.status not in [STATUS.OWNER, STATUS.ADMINISTRATOR]

async def isAdmin(filter, client, update):
    try:
        member = await client.get_chat_member(chat_id=update.chat.id, user_id=update.from_user.id)
    except FloodWait as wait_err:
        await asyncio.sleep(wait_err.value)
    except UserNotParticipant:
        return False
    except:
        return False

    return member.status in [STATUS.OWNER, STATUS.ADMINISTRATOR]

Member = filters.create(isMember)
Admin = filters.create(isAdmin)