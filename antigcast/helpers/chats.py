import asyncio
from pytz import timezone
from antigcast.helpers.database import *

from datetime import datetime
from dateutil.relativedelta import relativedelta

async def addGrupLangganan(chat_id, hari):
    now = datetime.now(timezone("Asia/Jakarta"))
    expired = now + relativedelta(days=int(hari))
    try:
        added = await add_actived_chat(int(chat_id))
        if added:
            await set_expired_date(int(chat_id), expired)
    except BaseException as e:
        print(e)