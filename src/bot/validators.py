
from aiogram.enums import ChatMemberStatus
from aiogram import Bot


VALID_STATUSES = (ChatMemberStatus.MEMBER, ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR)   

async def is_member_of(bot: Bot, tid: int, chat_id: int) -> bool:


    try:
        chat = await bot.get_chat_member(tid, chat_id)

        return chat.status in VALID_STATUSES
    except Exception as e:
        # print("kirekhar")
        # print(chat_id)
        # print(tid)
        # print(e)
        return False