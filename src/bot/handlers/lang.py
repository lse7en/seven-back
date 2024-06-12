from aiogram.filters import CommandObject
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.deep_linking import decode_payload
from aiogram.utils import formatting
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.models.user import User
from src.bot import beans
from src.bot.callbacks import community_callback, LanguageCallback
from src.bot.constants import START_PHOTO_FILE_ID
from src.bot.text import get_text


async def lang_handler(
    callback: CallbackQuery,
    callback_data: LanguageCallback,
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    """
    This handler receives messages with `/start` command
    """

    session = session_factory()
    user_repository = await beans.get_user_repository(session)

    async with session.begin():
        user = await user_repository.get_user_or_none_by_id(callback.from_user.id)
        user.language = callback_data.lang
        await user_repository.add_user(user)
        lang = user.language

    if not callback_data.next:
        await callback.answer(text="Done!", show_alert=False)
        await callback.bot.send_message(
            chat_id=callback.from_user.id,
            text=get_text(lang, "You have successfully changed your language!"),
        )

    else:
        await callback.answer(
            text=get_text(lang, "You have successfully changed your language!"),
            show_alert=False,
        )
        channel = InlineKeyboardButton(
            text="The lucky 7 Community", url="https://t.me/the_lucky_7"
        )
        joined = InlineKeyboardButton(
            text=get_text(lang, "Play"), url="https://t.me/the_lucky_7_bot/main"
        )

        kb = InlineKeyboardMarkup(inline_keyboard=[[channel], [joined]])

        caption = formatting.as_list(
            formatting.as_line(
                get_text(
                    lang, "Telegram channel owners can now receive 50% of ads revenue!"
                )
            ),
            formatting.as_line(
                get_text(
                    lang, "In Lucky 7, we give back 100% of our share to the members!"
                )
            ),
            formatting.as_line(
                get_text(
                    lang,
                    "Join our channel and invite your friends to increase your chance of winning one of the 7 giveaways!",
                ),
                "🎁",
                sep=" ",
            ),
            sep="\n\n",
        )

        await callback.bot.send_photo(
            chat_id=callback.from_user.id,
            photo=START_PHOTO_FILE_ID,
            reply_markup=kb,
            caption=caption.as_html(),
        )
