import asyncio
from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


async def stat_task(stat_bot: Bot, session_factory: async_sessionmaker[AsyncSession]) -> None:
    while True:
        
        print("I'm a task!")


        await asyncio.sleep(10)