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
from src.bot.validators import is_member_of
data_fake = [User(id=70056025, language='fa' )]


async def send_text_to_channel(
    bot: Bot, session_factory: async_sessionmaker[AsyncSession]
) -> None:

    photo_file = BufferedInputFile.from_file("/Users/xhsvn/Downloads/lll.jpg")

    botkb = InlineKeyboardButton(
        text="play", url="http://t.me/the_lucky_7_bot/main"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[[botkb]])

    caption = """
caption
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

    total = 7300
    step = 15
    invalid_uids = {93890907, 25621237}

    for i in range(0, total, step):
        async with session.begin():
            all_users = await user_repository.get_all_users_order_by_id_with_limit_offset(step, i)
        print(i , "to", i + step)
        for user in all_users:
            if user.id in invalid_uids:
                continue

            caption = formatting.as_list(formatting.as_line(
                "Introducing our next Contest: Lottery!💰 🎲",
                sep=" ",
            ),
            formatting.Url("https://t.me/the_lucky_7/54"),
            sep="\n\n",
            )
            try:
                await bot.send_message(
                    chat_id=user.id,
                    text=caption.as_html(),
                )
            except Exception as e:
                print(e)
                print(user.info)
            # wait 3 seconds to avoid spamming
        
        await asyncio.sleep(1)

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

    # set last secret code date to 1 day before current value of last secret code date
    async with session.begin():
        await session.execute(update(User).values(last_secret_code_date=func.date(User.last_secret_code_date) - 1))




async def add_lottery(
        bot: Bot, session_factory: async_sessionmaker[AsyncSession]
) -> None:
    session = session_factory()
    lottery_repo = LotteryRepository(session)

    async with session.begin():
        ticket_number = await lottery_repo.get_lottery_ticket_for_index(1, 7)
        print(ticket_number)
        
async def count_chan_users(
        bot: Bot, session_factory: async_sessionmaker[AsyncSession]
) -> None:
    session = session_factory()
    user_repo = UserRepository(session)

    total = 11000
    step = 500
    count = 2815

    for i in range(5000, total, step):
        async with session.begin():
            all_users = await user_repo.get_all_users_order_by_id_with_limit_offset(step, i)
        print(i, "to", i + step)
        for u_id in all_users:
            if await is_member_of(bot, COMMUNITY_TID, u_id):
                count += 1
        await asyncio.sleep(1)
        print(count)
    print("final count")
    print(count)


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

    stat_bot = Bot(
        "7120708074:AAHw_EKAlH1tJ0C_nJzubG9LvwSPZUZO7yU", parse_mode=ParseMode.HTML
    )
    engine, session_factory = setup_db()

    await send_text_to_channel(stat_bot, session_factory)


    await engine.dispose()
    await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
