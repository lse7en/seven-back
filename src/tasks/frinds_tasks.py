import asyncio
from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.repositories.user_repository import UserRepository
from src.repositories.system_repository import SystemRepository
from src.repositories.system_log_repository import SystemLogRepository
from src.bot.constants import STAT_CHAT_ID, JOIN_THREAD_ID, USER_LOG_THREAD_ID


async def friend_extra_check(session_factory: async_sessionmaker[AsyncSession], user_id: int) -> None:
 
    session = session_factory()
    user_repository = UserRepository(session)

    async with session.begin():

        ehsan = await user_repository.get_user(70056025)
        ehsan.points += 100

        await user_repository.add_user(ehsan)

    