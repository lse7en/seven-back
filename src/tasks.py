import asyncio
from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.repositories.user_repository import UserRepository
from src.repositories.system_repository import SystemRepository
from src.bot.constants import STAT_CHAT_ID, JOIN_THREAD_ID


async def stat_task(stat_bot: Bot, session_factory: async_sessionmaker[AsyncSession]) -> None:
    while True:
        
        session = session_factory()
        user_repository = UserRepository(session)
        system_repository = SystemRepository(session)
        async with session.begin():
            system = await system_repository.get()
            all_u = await user_repository.get_users_order_by_join_and_limit(system.last_user_log, system.max_user_cumulative)
            if all_u:
                system.last_user_log = all_u[-1].created_at
                await system_repository.update(system)
            
        if all_u:
            text = "\n\n".join([f"{i+1}. {user.full_info}" for i, user in enumerate(all_u)])
            try:
                await stat_bot.send_message(chat_id=STAT_CHAT_ID, message_thread_id=JOIN_THREAD_ID, text=text)
            except Exception as e:
                print(e)
        await asyncio.sleep(60)