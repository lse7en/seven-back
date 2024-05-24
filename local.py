import asyncio
from aiogram import Bot
from aiogram.enums import ParseMode
from src.core.database import setup_db
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.repositories.user_repository import UserRepository
from src.repositories.system_repository import SystemRepository
from src.bot.validators import is_member_of
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from src.bot.callbacks import community_callback
from aiogram.utils import formatting


from src.bot.constants import COMMUNITY_TID
from src.bot.text import get_text
from src.models.user import User


data_fake = [User(id=70056025, language='fa' )]


async def send_text_to_not_joined(
    bot: Bot, session_factory: async_sessionmaker[AsyncSession]
) -> None:
    session = session_factory()
    user_repository = UserRepository(session)
    async with session.begin():
        all_users = await user_repository.get_not_joined_users()

    for user in all_users:
        lang = user.language
        channel = InlineKeyboardButton(
            text="The lucky 7 Community", url="https://t.me/the_lucky_7"
        )
        joined = InlineKeyboardButton(
            text=get_text(lang, "Joined ✅"), callback_data=community_callback.pack()
        )

        kb = InlineKeyboardMarkup(inline_keyboard=[[channel], [joined]])

        caption = formatting.as_list(formatting.as_line(
            get_text(
                lang,
                "Just a reminder that you should also be a member of The Lucky 7 channel in order to participate in the giveaways and the $400 contest!",
            ),
            "🎁",
            sep=" ",
        ),
        formatting.Url("https://t.me/the_lucky_7/33"),
        sep="\n\n",
        )
        print(user.info)
        try:
            await bot.send_message(
                chat_id=user.id,
                reply_markup=kb,
                text=caption.as_html(),
            )
        except Exception as e:
            print(e)
        # wait 3 seconds to avoid spamming
        await asyncio.sleep(3)


async def send_contest_to_join(
    bot: Bot, session_factory: async_sessionmaker[AsyncSession]
) -> None:
    session = session_factory()
    user_repository = UserRepository(session)
    async with session.begin():
        all_users = await user_repository.get_joined_users()


    for user in all_users:
        lang = user.language


        caption = formatting.as_list(formatting.as_line(
            get_text(
                lang,
                "Check out our {} contest!",
            ).format("$400"),
            "💰",
            sep=" ",
        ),
        formatting.Url("https://t.me/the_lucky_7/33"),
        sep="\n\n",
        )
        print(user.info)
        try:
            await bot.send_message(
                chat_id=user.id,
                text=caption.as_html(),
            )
        except Exception as e:
            print(e)
        # wait 3 seconds to avoid spamming
        await asyncio.sleep(3)

async def print_users(
    bot: Bot, session_factory: async_sessionmaker[AsyncSession]
) -> None:
    session = session_factory()

    user_repository = UserRepository(session)
    async with session.begin():
        all_users = await user_repository.get_all_users()

        all_users = sorted(all_users, key=lambda x: x.points, reverse=True)
        for user in all_users:
            print(user.info)


async def get_rank_test(
    bot: Bot, session_factory: async_sessionmaker[AsyncSession]
) -> None:
    user_id = 307046083

    session = session_factory()
    user_repository = UserRepository(session)
    async with session.begin():
        all_u = await user_repository.get_all_users_with_ranking()
        min_invitation_for_top_4 = await user_repository.get_min_invitation_count_for_rank(9)
        print(all_u)
        print(min_invitation_for_top_4)


async def get_join_test(
    bot: Bot, session_factory: async_sessionmaker[AsyncSession]
) -> None:
    user_id = 307046083

    session = session_factory()
    user_repository = UserRepository(session)
    system_repository = SystemRepository(session)
    async with session.begin():
        system = await system_repository.get()
        all_u = await user_repository.get_users_order_by_join_and_limit(system.last_user_log, system.max_user_cumulative)
        if all_u:
            system.last_user_log = all_u[-1].created_at
            await system_repository.update(system)
        
    
    for i, user in enumerate(all_u):
        print(i, user.full_info, user.created_at)

async def main():
    print("This is a local script")
    print("It is not meant to be imported")
    password = input("Enter the password: ")
    if password == "11":
        print("You are in")
    else:
        print("You are out")
        return
    bot = Bot(
        "7047014378:AAFsQD5RJFgRUSQGIzRB2QKtGtliQH8_w5Q", parse_mode=ParseMode.HTML
    )
    engine, session_factory = setup_db()

    await get_join_test(bot, session_factory)


    await engine.dispose()
    await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
