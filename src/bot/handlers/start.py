from aiogram.filters import CommandObject
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.utils.deep_linking import decode_payload
from aiogram.utils import formatting
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.models.user import User
from src.bot import beans
from src.bot.callbacks import LanguageCallback


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
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    """
    This handler receives messages with `/start` command
    """

    session = session_factory()
    user_repository = await beans.get_user_repository(session)

    try:
        ref = int(decode_payload(command.args)) if command.args else None
    except Exception as e:
        ref = None

    async with session.begin():
        user = await user_repository.get_user_or_none_by_id(message.from_user.id)


    if not user:
        async with session.begin():
            new_user = User(
                    id=message.from_user.id,
                    referrer_id=ref,
                    first_name=message.from_user.first_name,
                    last_name=message.from_user.last_name,
                    username=message.from_user.username,
                    joined=False
                )
            await user_repository.add_user(new_user)

    await message.answer(
        reply_markup=kb,
        text=caption.as_html(),
    )
