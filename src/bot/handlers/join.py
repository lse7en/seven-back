from aiogram.types import CallbackQuery
from aiogram.utils import formatting
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from aiogram import Bot
from src.bot import beans
from src.bot.callbacks import JoinedCallback
from src.bot.constants import JOIN_PHOTO_FILE_ID
from src.bot.text import get_text
from src.bot.validators import is_member_of
from src.bot.constants import STAT_CHAT_ID, JOIN_THREAD_ID

async def joined_handler(
    callback: CallbackQuery,
    callback_data: JoinedCallback,
    stat_bot: Bot,
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    """
    This handler receives messages with `/start` command
    """

    session = session_factory()
    user_repository = await beans.get_user_repository(session)

    async with session.begin():
        lang = (
            await user_repository.get_user_or_none_by_id(callback.from_user.id)
        ).language
    tid = callback_data.tid

    if not await is_member_of(callback.bot, tid, callback.from_user.id):
        await callback.answer(
            text=get_text(lang, "You have not joined the channel! {}").format(tid),
            show_alert=True,
        )
        return

    try:
        await stat_bot.send_message(
            chat_id=STAT_CHAT_ID,
            message_thread_id=JOIN_THREAD_ID,
            text=f"New Sub: {callback.from_user.full_name} (@{callback.from_user.username}) id: {callback.from_user.id}"
        )
    except Exception as e:
        print(e)

    caption = formatting.as_list(
        formatting.Bold(get_text(lang, "Congratulations on joining! 🌟")),
        formatting.as_line(
            get_text(
                lang,
                "You now have a fantastic opportunity to be one of our lucky winners.",
            ),
            get_text(
                lang,
                "To increase your chances, invite your friends using your personal invitation link.",
            ),
            sep="\n",
        ),
        formatting.as_line(
            get_text(lang, "Simply type"),
            formatting.BotCommand("/invite"),
            get_text(lang, "to get your referral link and invite your friends."),
            sep=" ",
        ),
        formatting.as_line(
            get_text(lang, "Let's make our community bigger and better together! 🚀")
        ),
        sep="\n\n",
    )

    await callback.answer(
        text="You have successfully joined the channel!", show_alert=False
    )

    await callback.bot.send_photo(
        chat_id=callback.from_user.id,
        photo=JOIN_PHOTO_FILE_ID,
        caption=caption.as_html(),
    )
