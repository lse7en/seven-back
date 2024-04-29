from aiogram.types import Message
from aiogram.utils.markdown import hbold
from src.bot.permissions import IsChannelMember
from src.bot.constants import COMMUNITY_TID
from aiogram.utils import formatting
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.bot import beans


@IsChannelMember(COMMUNITY_TID)
async def score_handler(
    message: Message,
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    session = session_factory()
    user_repository = await beans.get_user_repository(session)

    async with session.begin():
        user = await user_repository.get_user_or_none_by_id(message.from_user.id)

    caption = formatting.as_list(
        formatting.Bold("🎉 Congratulations! 🎉"),
        formatting.as_list(
            f"You have invited {user.invited_users} friends.",
            formatting.as_line(
                "And now you have gathered",
                formatting.Italic(f"{user.points:.3f}"),
                "points so far!",
                sep=" ",
            ),
        ),
        sep="\n\n",
    )

    await message.answer(caption.as_html())
