from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.utils import formatting


from src.bot.callbacks import  LanguageCallback


fa_lang = InlineKeyboardButton(text="فارسی 🇮🇷", callback_data=LanguageCallback(lang='fa', next=False).pack())
en_lang = InlineKeyboardButton(text="English 🇺🇸", callback_data=LanguageCallback(lang='en', next=False).pack())
ru_lang = InlineKeyboardButton(text="Русский 🇷🇺", callback_data=LanguageCallback(lang='ru', next=False).pack())

kb = InlineKeyboardMarkup(inline_keyboard=[[en_lang, ru_lang, fa_lang]])


caption = formatting.as_list(
    formatting.Bold("Choose your language 🌐"),
    sep="\n\n",
)


async def language_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """


    await message.answer(
        reply_markup=kb,
        text=caption.as_html(),
    )



