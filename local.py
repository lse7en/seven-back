import asyncio
from aiogram import Bot
from aiogram.enums import ParseMode
from src.core.database import setup_db
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import delete, update, select, func
from src.repositories.user_repository import UserRepository
from src.repositories.lottery_repository import LotteryRepository
from src.repositories.system_repository import SystemRepository
from src.models.system_log import SystemLog
from src.bot.validators import is_member_of
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from src.bot.callbacks import community_callback
from aiogram.utils import formatting
from src.models.lottery import Lottery
from src.bot.validators import is_member_of
from src.bot.constants import COMMUNITY_TID
from src.bot.text import get_text
from src.models.user import User
from aiogram.types import BufferedInputFile

data_fake = [User(id=70056025, language='fa' )]


async def send_text_to_channel(
    bot: Bot, session_factory: async_sessionmaker[AsyncSession]
) -> None:

    photo_file = BufferedInputFile.from_file("/Users/xhsvn/Downloads/3 (1).jpg")

    botkb = InlineKeyboardButton(
        text="play", url="http://t.me/the_lucky_7_bot/main"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[[botkb]])

    caption = """
Oh look! 👀 There's a new mini-app! 😱

🥳 In order to make things easier and more appealing, we have now launched an exciting brand new mini-app! 🖥

💬 Get updated about ongoing contests, check your rank, invite and remind your friends to join, AND receive up to 300 extra points by clicking on the gift box! 🎁

⌛ The gift box takes a while to reload but by inviting each friend, you can cut the waiting time in half until you reach only 30 minutes! ✂️⏱
"""


    await bot.send_photo(
        photo=photo_file,
        chat_id='@the_lucky_7',
        reply_markup=kb,
        caption=caption,
    )
    # wait 3 seconds to avoid spamming
    await asyncio.sleep(3)



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
    limit = 50
    session = session_factory()
    user_repository = UserRepository(session)
    async with session.begin():
        users = await user_repository.get_top_users(limit)
    for u in users:
        print(u.info, u.static_rank)

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
    user_id = 70056025
    from datetime import datetime, timedelta, UTC
    session = session_factory()
    async with session.begin():
        await session.execute(update(User).values(last_lucky_push=datetime.now(UTC) - timedelta(days=1)).where(User.id == user_id))

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

async def check_is_member(
        bot: Bot, session_factory: async_sessionmaker[AsyncSession]
) -> None:
    user_id = 138599579
    session = session_factory()
    user_repository = UserRepository(session)
    
    j = await bot.get_chat_member(COMMUNITY_TID, user_id)
    print(j)


async def test_get_user(
        bot: Bot, session_factory: async_sessionmaker[AsyncSession]
) -> None:
    user_id = 98897584
    session = session_factory()
    user_repo = UserRepository(session)
    async with session.begin():
        user = await user_repo.get_user_or_none_by_id(user_id)
        print(user.full_info)

async def set_static_rank(
        bot: Bot, session_factory: async_sessionmaker[AsyncSession]
) -> None:
    session = session_factory()
    user_repo = UserRepository(session)
    async with session.begin():
        await user_repo.set_static_rank_for_all()


async def cheat(
        bot: Bot, session_factory: async_sessionmaker[AsyncSession]
) -> None:
    user_id = 70056025
    session = session_factory()
    user_repo = UserRepository(session)
    from datetime import date
    old_date = date(2021, 1, 1)
    async with session.begin():
        user = await user_repo.get_user_or_none_by_id(user_id)
        print(user.last_secret_code_date)
        user.invited_users += 5
        user.points += 10000
        await user_repo.add_user(user)
        # user.last_secret_code_date = old_date
        # await user_repo.add_user(user)


async def add_lottery(
        bot: Bot, session_factory: async_sessionmaker[AsyncSession]
) -> None:
    session = session_factory()
    lottery_repo = LotteryRepository(session)

    async with session.begin():
        ticket_number = await lottery_repo.get_lottery_ticket_for_index(1, 7)
        print(ticket_number)
        



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

    await cheat(bot, session_factory)


    await engine.dispose()
    await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
