from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.bot.permissions import IsChannelMember
from src.bot.constants import COMMUNITY_TID
from aiogram.utils import formatting
from aiogram.utils.deep_linking import create_start_link
from src.bot.text import get_text
from src.bot import beans
random_string = '1234567890abcdefghijklmnopqrstuvwxyz'


 
@IsChannelMember(COMMUNITY_TID)
async def invite_handler(message: Message, session_factory: async_sessionmaker[AsyncSession],
) -> None:
    session = session_factory()
    user_repository = await beans.get_user_repository(session)


    async with session.begin():
        lang = (await user_repository.get_user_or_none_by_id(message.from_user.id)).language
    
    link = await create_start_link(message.bot, payload=str(message.from_user.id), encode=True)

    caption = formatting.as_list(
    formatting.as_line(
        formatting.Spoiler(get_text(lang, "Telegram premium")),
        formatting.Spoiler(get_text(lang, "100% Share of ad revenue")),
        sep="\n",
    ),
    formatting.Url(link),
    formatting.HashTag("WeGiveBack"),
    sep="\n\n",
)



    await message.answer(caption.as_html())