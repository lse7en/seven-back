from aiogram.filters import CommandObject
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.deep_linking import decode_payload
from aiogram.utils import formatting
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.models.user import User
from src.bot import beans
from src.bot.callbacks import community_callback, LanguageCallback
from src.bot.constants import START_PHOTO_FILE_ID, ADMIN_CHAT_ID
from src.bot.text import get_text


async def lang_handler(
    callback: CallbackQuery, callback_data: LanguageCallback,
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
        await callback.answer(text=get_text(lang, "You have successfully changed your language!"), show_alert=False)
        channel = InlineKeyboardButton(
        text="The lucky 7 Community", url="https://t.me/the_lucky_7"
        )
        joined = InlineKeyboardButton(text=get_text(lang, "Joined ✅"), callback_data=community_callback.pack())

        kb = InlineKeyboardMarkup(inline_keyboard=[[channel], [joined]])


        caption = formatting.as_list(
            formatting.Bold(get_text(lang,"🚀 Exciting News! 🚀")),
            formatting.as_line(
                get_text(lang, "Starting this month, Telegram has introduced a fantastic new feature allowing channel owners to earn revenue through ads. But here’s the twist: we're giving 100% of our ad revenue back to you, our lovely community!")),
            formatting.as_marked_section(
                get_text(lang, "Here's how it works:"),
                get_text(lang, "Every month, 100% of our ad revenue will be shared among 7 lucky subscribers."),
                get_text(lang, "The winners will be selected randomly, ensuring that everyone has a fair chance to win."),
            ),
            formatting.as_line(
                get_text(lang, "Stay subscribed and active for your chance to be one of the lucky 7! 🤑")
            ),
            sep="\n\n",
        )

        await callback.bot.send_photo(
            chat_id=callback.from_user.id,
            photo=START_PHOTO_FILE_ID,
            reply_markup=kb,
            caption=caption.as_html(),
        )




