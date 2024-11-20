from aiogram.types import Message
from aiogram.filters import CommandObject
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.bot import beans
from src.bot.constants import COMMUNITY_TID
from src.bot.permissions import HasPermissions


# get daily active users
@HasPermissions(2)
async def dit_handler(
    message: Message,
    command: CommandObject,
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    try:
        uid = int(command.args)

        user_repository = await beans.get_user_repository(session_factory)

        mem = await message.bot.get_chat_member(COMMUNITY_TID, uid)
        name = mem.user.full_name
        username = mem.user.username
        status = mem.status

        u = await user_repository.get_user_or_none_by_id(uid)

        await message.answer(
            f"User: {name}\nUsername: @{username}\nStatus: {status}\n last check in: {u.last_check_in}"
        )
    except Exception as e:
        await message.answer(f"Error: {e}")
