import asyncio
from aiogram import Bot
from aiogram.enums import ParseMode
from src.core.database import setup_db
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import delete, update
from src.repositories.user_repository import UserRepository
from src.repositories.system_repository import SystemRepository
from src.models.system_log import SystemLog
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

async def get_leaderboard_test(
    bot: Bot, session_factory: async_sessionmaker[AsyncSession]
) -> None:
    limit = 20
    session = session_factory()
    user_repository = UserRepository(session)
    async with session.begin():
        all_u = await user_repository.get_users_with_ranking(limit)
        users = await user_repository.get_users_with_ids_in(all_u)
    for u in users:
        print(u)
        print(type(u))
        if getattr(u, 'info', None) is None:
            print("no info")
        else:
            print(u.info)

async def get_user_photo_test(
    bot: Bot, session_factory: async_sessionmaker[AsyncSession]
) -> None:
    user_id = 70056025


    p = await bot.get_user_profile_photos(user_id, limit=1)

    if p.total_count > 0:
        candid = min(p.photos[0], key=lambda x: x.width)
        file_id = candid.file_id

        photo = await bot.get_file(file_id)
        await bot.download_file(photo.file_path, "photo.jpg")
        print(photo.file_path)
        print("kir")
        # with open("photo.jpg", "wb") as f:
        #     await 

async def test_get_friends(
        bot: Bot, session_factory: async_sessionmaker[AsyncSession]
) -> None:
    user_id = 5824417928
    session = session_factory()
    user_repository = UserRepository(session)
    async with session.begin():
        user = await user_repository.get_user_or_none_by_id(user_id)
        print(user.info)
        await user_repository.session.execute(delete(SystemLog).where(SystemLog.user_id == user_id))
        await user_repository.session.delete(user)

async def reset_last_lucky_push(
        bot: Bot, session_factory: async_sessionmaker[AsyncSession]
) -> None:
    user_id = 5824417928
    from datetime import datetime, timedelta, UTC
    session = session_factory()
    async with session.begin():
        await session.execute(update(User).values(last_lucky_push=datetime.now(UTC) - timedelta(days=1)))

async def test_edit_me(
        bot: Bot, session_factory: async_sessionmaker[AsyncSession]
) -> None:
    user_id = 70056025
    from datetime import datetime, timedelta, UTC
    session = session_factory()
    user_repository = UserRepository(session)
    async with session.begin():
        user = await user_repository.get_user_or_none_by_id(user_id)
        user.joined = False
        user.last_lucky_push = datetime.now(UTC) - timedelta(days=1)
        await user_repository.add_user(user)

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

    await test_edit_me(bot, session_factory)


    await engine.dispose()
    await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
