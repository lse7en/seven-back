from aiogram.types import Message
from aiogram.utils.markdown import hbold
from src.bot.permissions import IsChannelMember
from src.bot.constants import COMMUNITY_TID
from aiogram.utils import formatting
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.bot import beans
from src.bot.text import get_text

@IsChannelMember(COMMUNITY_TID)
async def rank_handler(
    message: Message,
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    session = session_factory()
    # user_repository = await beans.get_user_repository(session)

    # async with session.begin():
    #     user = await user_repository.get_user_or_none_by_id(message.from_user.id)
    #     lang = user.language





    # caption = formatting.as_line(
    #         get_text(lang, "You are now ranked number {} on the leaderboard! By inviting {} more friends, you'll be ranked 1st!").format(user.invited_users),
    # )

    # await message.answer(caption.as_html())
