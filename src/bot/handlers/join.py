from aiogram.types import CallbackQuery
from aiogram.utils import formatting
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.bot import beans
from src.bot.callbacks import JoinedCallback
from src.bot.constants import JOIN_PHOTO_FILE_ID
from src.bot.text import get_text
from src.bot.validators import is_member_of


async def joined_handler(
    callback: CallbackQuery,
    callback_data: JoinedCallback,
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    """
    This handler receives messages with `/start` command
    """

    session = session_factory()
    user_repository = await beans.get_user_repository(session)

    async with session.begin():
        user = await user_repository.get_user_or_none_by_id(callback.from_user.id)
        info = user.info
        lang = user.language
    tid = callback_data.tid

    if not await is_member_of(callback.bot, tid, callback.from_user.id):
        await callback.answer(
            text=get_text(lang, "You have not joined the channel! {}").format(tid),
            show_alert=True,
        )
        return
    if not user.joined:
        async with session.begin():
            user.joined = True
            if user.referrer_id and not user.tasks_join_channel:
                referrer = await user_repository.get_user_or_none_by_id(user.referrer_id)
                referrer.invited_users += 1
                referrer.points += 1000
                await user_repository.add_user(referrer)
            await user_repository.add_user(user)
        
        if user.referrer_id and not user.tasks_join_channel:
            joined_message = formatting.as_list(
                formatting.as_line(formatting.Bold(get_text(referrer.language, "Keep going!")), "💪", sep=" "),
                formatting.as_line(
                    get_text(referrer.language, "Your friend"),
                    formatting.Bold(user.full_name),
                    get_text(referrer.language, "joined the Bot!"),
                    sep=" ",
                ),
                formatting.as_list(
                    get_text(referrer.language, "You have invited {} friends.").format(referrer.invited_users),
                    formatting.as_line(
                        get_text(referrer.language, "And you have gathered"),
                        formatting.Italic(f"{referrer.points}"),
                        get_text(referrer.language, "points so far!"),
                        sep=" ",
                    ),
                ),
                sep="\n\n",
            )

            await callback.bot.send_message(
                chat_id=referrer.id,
                **joined_message.as_kwargs(),
            )


    caption = formatting.as_list(
        formatting.as_line(
            formatting.Bold(get_text(lang, "Welcome aboard!")),
            "🎆",
            sep=" ",
        ),
        formatting.as_list(
            formatting.as_line(
                get_text(
                    lang,
                    "You are now one step closer to becoming one of the Lucky 7 winners!",
                ),
                "🏅",
                sep=" ",
            ),
            formatting.as_line(
                get_text(lang, "To increase your chances, get your own referral link from"),
                formatting.BotCommand("/invite"),
                get_text(lang, "and send it to as many friends you can!"),
                "🔠",
                sep=" ",
            ),
            sep="\n",
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
