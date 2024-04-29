from aiogram.filters import CommandObject
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.utils.deep_linking import decode_payload
from aiogram.utils import formatting
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.models.user import User
from src.bot import beans
from src.bot.callbacks import community_callback
from src.bot.constants import START_PHOTO_FILE_ID, ADMIN_CHAT_ID

channel = InlineKeyboardButton(
    text="The lucky 7 Community", url="https://t.me/the_lucky_7"
)
joined = InlineKeyboardButton(text="Joined ✅", callback_data=community_callback.pack())

kb = InlineKeyboardMarkup(inline_keyboard=[[channel], [joined]])


caption = formatting.as_list(
    formatting.Bold("🚀 Exciting News! 🚀"),
    formatting.as_line(
        "Starting this month, Telegram has introduced a fantastic new feature allowing channel owners to earn revenue through ads. But here’s the twist: we're giving 100% of our ad revenue back to you, our lovely community!"
    ),
    formatting.as_marked_section(
        "Here's how it works:",
        "Every month, 100% of our ad revenue will be shared among 7 lucky subscribers.",
        "The winners will be selected randomly, ensuring that everyone has a fair chance to win.",
    ),
    formatting.as_line(
        "Stay subscribed and active for your chance to be one of the lucky 7! 🤑"
    ),
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

    await message.answer_photo(
        photo=START_PHOTO_FILE_ID,
        reply_markup=kb,
        caption=caption.as_html(),
    )

    if not user:
        await message.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"New user: {message.from_user.full_name} (@{message.from_user.username})"
        )


    if referrer and not user:
        joined_message = formatting.as_list(
            formatting.Bold("🎉 Congratulations! 🎉"),
            formatting.as_line(
                "Your friend",
                formatting.Bold(message.from_user.first_name),
                "joined the Bot!",
                sep=" ",
            ),
            formatting.as_list(
                f"You have invited {referrer.invited_users} friends.",
                formatting.as_line(
                    "And now you have gathered",
                    formatting.Italic(f"{referrer.points:.3f}"),
                    "points so far!",
                    sep=" ",
                ),
            ),
            sep="\n\n",
        )

        await message.bot.send_message(
            chat_id=referrer.id,
            **joined_message.as_kwargs(),
        )


