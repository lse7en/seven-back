from aiogram.types import Message
from aiogram.utils.markdown import hbold
from src.bot.permissions import IsChannelMember
from src.bot.constants import COMMUNITY_TID, STAT_CHAT_ID, USER_LOG_THREAD_ID
from aiogram.utils import formatting
from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.bot import beans
from src.bot.text import get_text

@IsChannelMember(COMMUNITY_TID)
async def rank_handler(
    message: Message,
    stat_bot: Bot,
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    session = session_factory()
    user_repository = await beans.get_user_repository(session)

    async with session.begin():
        user = await user_repository.get_user_or_none_by_id(message.from_user.id)
        lang = user.language



    if user.invited_users >= 7:
        # rank = await user_repository.get_user_rank(user.id)
        rank = user.static_rank

        if rank < 20:
            caption = formatting.as_list(
                formatting.as_line("⚡️", get_text(lang, "Hooray!"), get_text(lang, "You are now ranked number {} on the leaderboard!").format(rank), sep=" "),
                get_text(lang, "Keep inviting your friends to secure your spot at the top!"),
                sep="\n",
            )

            
        else:
            min_invitations = await user_repository.get_min_invitation_count_for_rank(20)

            caption = formatting.as_list(
                formatting.as_line(get_text(lang, "You are now ranked number {} on the leaderboard!").format(rank), sep=" "),
                formatting.as_line(get_text(lang, "By inviting {} more friends, you will be in the top 20.").format(min_invitations - user.invited_users), "👏🏻", sep=" "),
                formatting.as_line(get_text(lang, "Get going!"), "💪🏻", formatting.BotCommand("/invite"), sep=" "),
                sep="\n",
            )


    else:
        caption = formatting.as_list(
            formatting.as_list("⚠️",
            get_text(lang, "You need to invite at least 7 friends in order to participate in the contest and be ranked."), sep=" "),
            formatting.as_line(get_text(lang, "Get started!"), formatting.BotCommand("/invite"), sep=" "),
            sep="\n\n",
        )
    await message.answer(caption.as_html())
    try:
        await stat_bot.send_message(chat_id=STAT_CHAT_ID, message_thread_id=USER_LOG_THREAD_ID, text=f"command: /rank\nuser: {user.info}")
    except Exception as e:
        print(e)