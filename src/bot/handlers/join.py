from aiogram.types import CallbackQuery
from src.bot.callbacks import JoinedCallback
from src.bot.validators import is_member_of
from src.bot.constants import JOIN_PHOTO_FILE_ID
from aiogram.utils import formatting

caption = formatting.as_list(
    formatting.Bold("Congratulations on joining! 🌟"),
    formatting.as_line(
        "You now have a fantastic opportunity to be one of our lucky winners.",
        "To increase your chances, invite your friends using your personal invitation link.",
        sep="\n",
    ),
    formatting.as_line(
        "Simply type",
        formatting.BotCommand("/invite"),
        "to get your referral link and invite your friends.",
        sep=" ",
    ),
    formatting.as_line("Let's make our community bigger and better together! 🚀"),
    sep="\n\n",
)


async def joined_handler(
    callback: CallbackQuery, callback_data: JoinedCallback
) -> None:
    tid = callback_data.tid

    if not await is_member_of(callback.bot, tid, callback.from_user.id):
        await callback.answer(
            text="You have not joined the channel! {}".format(tid), show_alert=True
        )
        return

    await callback.answer(text="You have successfully joined the channel!", show_alert=False)

    await callback.bot.send_photo(
        chat_id=callback.from_user.id,
        photo=JOIN_PHOTO_FILE_ID,
        caption=caption.as_html(),
    )
