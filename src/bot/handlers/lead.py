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

    if lead > 40:
        lead = 40

    async with session.begin():
        users = await user_repository.get_top_users(lead)

        text = "\n\n".join(
            [
                f"{i+1}. {user.info}"
                for i, user in enumerate(users)
            ]
        )

    await message.answer(text)
