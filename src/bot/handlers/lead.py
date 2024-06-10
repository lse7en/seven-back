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

@HasPermissions(2)
async def lead_handler(
    message: Message,
    command: CommandObject,
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    session = session_factory()
    user_repository = await beans.get_user_repository(session)

    try:
        lead = int(command.args) if command.args else 10
    except Exception as e:
        lead = 10


    async with session.begin():
        all_u = await user_repository.get_users_with_ranking(lead)
        users = await user_repository.get_users_with_ids_in(all_u)

        text = "\n\n".join(
            [
                f"{i+1}. {user.info}"
                for i, user in enumerate(users)
            ]
        )

    await message.answer(text)
