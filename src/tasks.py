import asyncio
from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


async def stat_task(stat_bot: Bot, session_factory: async_sessionmaker[AsyncSession]) -> None:
    pass
    # while True:
    #     print('My Task')
    #     await asyncio.sleep(10)