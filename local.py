

import asyncio
from aiogram import Bot
from aiogram.enums import ParseMode
from src.core.database import setup_db
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.repositories.user_repository import UserRepository
from src.bot.validators import is_member_of

from src.bot.constants import COMMUNITY_TID
async def populate_data(bot: Bot, session_factory: async_sessionmaker[AsyncSession]) -> None:

    session = session_factory()

    user_repository = UserRepository(session)
    async with session.begin():
        all_users = await user_repository.get_all_users()

        for user in all_users:
            # user_chat = await bot.get_chat(chat_id=user.id)
            # user.username = user_chat.username
            # user.first_name = user_chat.first_name
            # user.last_name = user_chat.last_name
            # user.joined = await is_member_of(bot, COMMUNITY_TID, user.id)
            # await user_repository.add_user(user)


            print(user.info)


async def get_rank_test(bot: Bot, session_factory: async_sessionmaker[AsyncSession]) -> None:
    user_id = 307046083

    session = session_factory()
    user_repository = UserRepository(session)
    async with session.begin():
        rank = await user_repository.get_user_rank(user_id)
        print(rank)



async def main():
    print('This is a local script')
    print('It is not meant to be imported')
    password = input('Enter the password: ')
    if password == '11':
        print('You are in')
    else:
        print('You are out')
        return
    bot = Bot("7047014378:AAFsQD5RJFgRUSQGIzRB2QKtGtliQH8_w5Q", parse_mode=ParseMode.HTML)
    engine, session_factory = setup_db()


    await populate_data(bot, session_factory)



    await engine.dispose()
    await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
