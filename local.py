# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "locals",
# ]
# ///
import asyncio
from aiogram.client.default import DefaultBotProperties

from aiogram import Bot
from aiogram.enums import ParseMode
from src.core.database import setup_db
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import delete, update, select
from src.repositories.user_repository import UserRepository
from src.repositories.lottery_repository import LotteryRepository
from src.repositories.system_repository import SystemRepository
from src.models.system_log import SystemLog
from src.bot.validators import is_member_of
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import formatting
from src.models.lottery import Ticket, Participant
from src.bot.constants import COMMUNITY_TID
from src.bot.text import get_text
from src.models.user import User
from src.models.lottery import Lottery
from aiogram.types import BufferedInputFile
from src.schemas.lottery_schema import Ticket as TicketSchema


data_fake = [User(id=70056025, language="fa")]


async def send_text_to_channel(
    bot: Bot, session_factory: async_sessionmaker[AsyncSession]
) -> None:
    photo_file = BufferedInputFile.from_file("/Users/xhsvn/Downloads/nov07b.png")

    botkb = InlineKeyboardButton(text="play", url="http://t.me/the_lucky_7_bot/main")
    kb = InlineKeyboardMarkup(inline_keyboard=[[botkb]])

    caption = """
caption
"""

    await bot.send_photo(
        photo=photo_file,
        chat_id="@the_lucky_7",
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


        kb = InlineKeyboardMarkup(inline_keyboard=[[channel]])

        caption = formatting.as_list(
            formatting.as_line(
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

    total = 21300
    step = 20
    invalid_uids = {93890907, 25621237}
    error_count = 0

    for i in range(680, total, step):
        async with session.begin():
            all_users = (
                await user_repository.get_all_users_order_by_id_with_limit_offset(
                    step, i
                )
            )
        print(i, "to", i + step, "error_count", error_count)
        for u_id in all_users:
            if u_id in invalid_uids:
                continue

            caption = formatting.as_list(
                formatting.as_line(
                    "💰 $1000 Lottery! And 🎲 6 time higher chance of winning ...",
                    sep=" ",
                ),
                formatting.Url("https://t.me/the_lucky_7/147"),
                sep="\n\n",
            )
            try:
                await bot.send_message(
                    chat_id=u_id,
                    text=caption.as_html(),
                )
            except Exception as e:
                error_count += 1
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
        min_invitation_for_top_4 = (
            await user_repository.get_min_invitation_count_for_rank(9)
        )
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
        all_u = await user_repository.get_users_order_by_join_and_limit(
            system.last_user_log, system.max_user_cumulative
        )
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
        await user_repository.session.execute(
            delete(SystemLog).where(SystemLog.user_id == user_id)
        )
        await user_repository.session.delete(user)


async def reset_last_lucky_push(
    bot: Bot, session_factory: async_sessionmaker[AsyncSession]
) -> None:
    user_id = 70056025
    from datetime import datetime, timedelta, UTC

    session = session_factory()
    async with session.begin():
        await session.execute(
            update(User)
            .values(last_lucky_push=datetime.now(UTC) - timedelta(days=1))
            .where(User.id == user_id)
        )


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


async def cheat(bot: Bot, session_factory: async_sessionmaker[AsyncSession]) -> None:
    uids = [100084659, 70056025]

    session = session_factory()
    user_repo = UserRepository(session)

    from datetime import datetime, timedelta, UTC
    # set last secret code date to 1 day before current value of last secret code date

    for user_id in uids:
        async with session.begin():
            user = await user_repo.get_user_or_none_by_id(user_id)
            # user.invited_users = user.invited_users + 4
            user.last_secret_code_date = datetime.now(UTC) - timedelta(days=2)
            user.last_ads_watch_for_points = datetime.now(UTC) - timedelta(minutes=32)
            await user_repo.add_user(user)


async def add_lottery(
    bot: Bot, session_factory: async_sessionmaker[AsyncSession]
) -> None:
    session = session_factory()
    lottery_repo = LotteryRepository(session)
    import random
    tickets = random.sample(range(6**7), 6**7)

    print(len(tickets))
    print(6**7)
    print(tickets[:10])

    from datetime import datetime, UTC

    dt = datetime(2024, 11, 17, 16, 0, 0, 0, UTC)
    # lottery_id = 6
    # print(dt)
    async with session.begin():
        lottery = Lottery(name="arc 1: 0", pot=1000, draw_date=dt, tickets=tickets, jackpot=None)
        await lottery_repo.add_lottery(lottery)

        # random_ticket = await lottery_repo.get_lottery_ticket_for_index(lottery_id, 1)
        # print(random_ticket)

        # random_ticket = await lottery_repo.get_lottery_ticket_for_index(lottery_id, 2)
        # print(random_ticket)
        # random_ticket = await lottery_repo.get_lottery_ticket_for_index(lottery_id, 4)
        # print(random_ticket)


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
            all_users = await user_repo.get_all_users_order_by_id_with_limit_offset(
                step, i
            )
        print(i, "to", i + step)
        for u_id in all_users:
            if await is_member_of(bot, COMMUNITY_TID, u_id):
                count += 1
        await asyncio.sleep(1)
        print(count)
    print("final count")
    print(count)


async def get_lottery_winners(
    bot: Bot, session_factory: async_sessionmaker[AsyncSession]
) -> None:
    session = session_factory()

    lottery_id = 12
    wining_draw = "3616144"


    async with session.begin():
        tickets = await session.execute(
            select(Ticket).where(Ticket.lottery_id == lottery_id)
        )

        tickets = tickets.scalars().all()

        print(len(tickets))

        for ticket in tickets:
            ts = TicketSchema.model_validate(ticket, from_attributes=True)

            if ts.ticket[6] == wining_draw[6]:
                mt = 0
                for i in range(7):
                    if ts.ticket[i] == wining_draw[i]:
                        mt += 1
                if mt >= 5:
                    print(ts.ticket, mt, ticket.user_id)


    # u_ids = [302503930, 1023145865]
    # tickets = [124476, 130944]

    # pr = ParticipantRepository(session)
    # async with session.begin():

    #     for uid in u_ids:
    #         p = await pr.get_participant(uid, lottery_id)
    #         p.lottery.jackpot = 124572
    #         print(p.user.info)
    #         p.wins = 5000
    #         for t in p.tickets:
    #             if t.ticket_number in tickets:
    #                 t.win = 5000
    #                 t.matched = 5
    #         session.add(p)
            



async def make_myself_winner(
    bot: Bot, session_factory: async_sessionmaker[AsyncSession]
) -> None:
    session = session_factory()

    lottery_id = 1
    user_id = 70056025

    async with session.begin():
        tickets = (
            await session.execute(
                select(Ticket).where(
                    Ticket.lottery_id == lottery_id, Ticket.user_id == user_id
                )
            )
        ).scalars()
        tickets = list(tickets.all())[:5]

        for ticket in tickets:
            ticket.win = 300
        
        session.add_all(tickets)

        p = (await session.execute(select(Participant).where(Participant.user_id == user_id, Participant.lottery_id  == lottery_id))).scalar_one()
        p.wins = 120
        session.add(p)


import sqlalchemy as sa

async def get_dummy_users(
    bot: Bot, session_factory: async_sessionmaker[AsyncSession]
) -> None:
    session = session_factory()
    user_repo = UserRepository(session)

    async with session.begin():
        fa_users = list((await session.scalars(
            sa.select(User).where(User.language == 'fa').order_by(User.last_check_in.asc()).limit(10)
        )).all())

        en_users = list((await session.scalars(
            sa.select(User).where(User.language == 'en').order_by(User.last_check_in.asc()).limit(15)
        )).all())

        ru_users = list((await session.scalars(
            sa.select(User).where(User.language == 'ru').order_by(User.last_check_in.asc()).limit(15)
        )).all())

        print('fa users', len(fa_users), "en users", len(en_users), "ru users", len(ru_users))


        for u in fa_users + en_users + ru_users:
            print(f"User(id=-{u.id}, first_name={u.first_name}, last_name={u.last_name}, ),")




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
        "7047014378:AAFsQD5RJFgRUSQGIzRB2QKtGtliQH8_w5Q", default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    stat_bot = Bot(
        "7120708074:AAHw_EKAlH1tJ0C_nJzubG9LvwSPZUZO7yU", default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    engine, session_factory = setup_db()

    await get_dummy_users(bot, session_factory)

    await engine.dispose()
    await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
