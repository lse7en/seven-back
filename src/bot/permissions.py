from functools import wraps
# import os
# from telegram import Update
from aiogram import Bot

from src.bot.validators import is_member_of
admin_lvls = {
    70056025: 0,
    1112295397: 1,
    307046083: 2,
    100084659: 3,
    133489884: 3
}


def get_admin_rank(chat_id: int) -> int:
    return admin_lvls.get(chat_id, 1000)


def is_admin(chid, rank: int) -> bool:
    admin_rank = get_admin_rank(chid)
    
    return admin_rank <= rank


class HasPermissions:
    
    def __init__(self, level: int):
        self.level = level
    
    def __call__(self, func):
        
        @wraps(func)
        async def permission(*args, **kwargs):
            message = args[0]
            if is_admin(message.from_user.id, self.level):
                return await func(*args, **kwargs)
            else:
                await message.answer("You do not have permission to do that")
            
        return permission




class IsChannelMember:

    def __init__(self, tid: int):
        self.tid = tid
    
    def __call__(self, func):
        
        @wraps(func)
        async def permission(*args, **kwargs):
            
            message = args[0]
            bot: Bot = message.bot

            if not await is_member_of(bot, self.tid, message.chat.id):
                await message.answer("You must be a member of the channel to use this command: @the_lucky_7")
                return

            
            return await func(*args, **kwargs)

            
        return permission
