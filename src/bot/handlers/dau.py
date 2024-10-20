from aiogram.types import Message
from aiogram.filters import CommandObject

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.bot import beans
from src.bot.permissions import HasPermissions


# get daily active users
@HasPermissions(2)
async def dau_handler(
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

    await message.answer(f"Active users in the last {hours} hours: {count}")
