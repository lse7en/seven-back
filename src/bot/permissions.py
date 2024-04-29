from functools import wraps
# import os
# from telegram import Update
from aiogram import Bot

from src.bot.validators import is_member_of
admin_lvls = {
    70056025: 0,
    1112295397: 1,
    100084659: 2,
    133489884: 2
}


def get_admin_rank(chat_id: int) -> int:
    return admin_lvls.get(chat_id, 1000)


def is_admin(update, rank: int) -> bool:
    admin_rank = get_admin_rank(update.message.chat_id)
    
    return admin_rank <= rank


class HasPermissions:
    
    def __init__(self, level: int):
        self.level = level
    
    def __call__(self, func):
        
        @wraps(func)
        async def permission(*args, **kwargs):
            # update = args[0]
            return await func(*args, **kwargs)
            # if is_admin(update, self.level):
            #     return await func(*args, **kwargs)
            # else:
            #     await update.message.reply_text("You do not have permission to do that")
            
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
                await message.answer("You must be a member of the channel to use this command")
                return

            
            return await func(*args, **kwargs)

            
        return permission
