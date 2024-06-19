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
@HasPermissions(2)
async def dau(
    message: Message,
    command: CommandObject,
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    session = session_factory()
    user_repository = await beans.get_user_repository(session)

    try:
        hours = int(command.args) if command.args else 24
    except Exception as e:
        hours = 24



    async with session.begin():
        count = await user_repository.count_active_users_since_last_hour(hours)

    await message.answer(count)
