from aiogram.types import Message
from aiogram.utils.markdown import hbold
from src.bot.permissions import IsChannelMember
from aiogram.filters import CommandObject

from src.bot.constants import COMMUNITY_TID
from aiogram.utils import formatting
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.bot import beans
from src.bot.text import get_text
from src.bot.permissions import HasPermissions


# get daily active users
@HasPermissions(0)
async def dit_handler(
    message: Message,
    command: CommandObject,
) -> None:

    try:
        uid = int(command.args)


        mem = await message.bot.get_chat_member(COMMUNITY_TID, uid)
        name = mem.user.full_name
        username = mem.user.username
        status = mem.status

        await message.answer(f"User: {name}\nUsername: {username}\nStatus: {status}")
    except Exception as e:
        await message.answer(f"Error: {e}")
    
