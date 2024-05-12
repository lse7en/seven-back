from aiogram.filters import CommandObject
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.utils.deep_linking import decode_payload
from aiogram.utils import formatting
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from aiogram import Bot
from src.models.user import User
from src.bot import beans
from src.bot.callbacks import LanguageCallback
from src.bot.constants import ADMIN_CHAT_ID, STAT_CHAT_ID, JOIN_THREAD_ID
from src.bot.text import get_text

fa_lang = InlineKeyboardButton(text="فارسی 🇮🇷", callback_data=LanguageCallback(lang='fa', next=True).pack())
en_lang = InlineKeyboardButton(text="English 🇺🇸", callback_data=LanguageCallback(lang='en', next=True).pack())
ru_lang = InlineKeyboardButton(text="Русский 🇷🇺", callback_data=LanguageCallback(lang='ru', next=True).pack())

kb = InlineKeyboardMarkup(inline_keyboard=[[en_lang], [ru_lang], [fa_lang]])


caption = formatting.as_list(
    formatting.Bold("Choose your language 🌐"),
    sep="\n\n",
)


async def start_handler(
    message: Message,
    command: CommandObject,
    stat_bot: Bot,
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    """
    This handler receives messages with `/start` command
    """

    session = session_factory()
    user_repository = await beans.get_user_repository(session)

    ref = int(decode_payload(command.args)) if command.args else None

    async with session.begin():
        user = await user_repository.get_user_or_none_by_id(message.from_user.id)
        referrer = (
            await user_repository.get_user_or_none_by_id(int(ref)) if ref else None
        )

    if not user:
        async with session.begin():
            await user_repository.add_user(
                User(
                    id=message.from_user.id,
                    invited_by_id=referrer.id if referrer else None,
                )
            )
            if referrer:
                referrer.invited_users += 1
                await user_repository.add_user(referrer)

    await message.answer(
        reply_markup=kb,
        text=caption.as_html(),
    )

    if not user:
        try:

            text = f"New user: {message.from_user.full_name} (@{message.from_user.username}) id: {message.from_user.id}, ref: {referrer.id if referrer else None}"

            await stat_bot.send_message(
                chat_id=STAT_CHAT_ID,
                message_thread_id=JOIN_THREAD_ID,
                text=text
            )
        except Exception as e:
            print(e)


    if referrer and not user:
        lang = referrer.language
        joined_message = formatting.as_list(
            formatting.Bold(get_text(lang, "🎉 Congratulations! 🎉")),
            formatting.as_line(
                get_text(lang, "Your friend"),
                formatting.Bold(message.from_user.first_name),
                get_text(lang, "joined the Bot!"),
                sep=" ",
            ),
            formatting.as_list(
                get_text(lang, "You have invited {} friends.").format(referrer.invited_users),
                formatting.as_line(
                    get_text(lang, "And now you have gathered"),
                    formatting.Italic(f"{referrer.points:.3f}"),
                    get_text(lang, "points so far!"),
                    sep=" ",
                ),
            ),
            sep="\n\n",
        )

        await message.bot.send_message(
            chat_id=referrer.id,
            **joined_message.as_kwargs(),
        )

