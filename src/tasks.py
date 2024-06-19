import asyncio
from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.repositories.user_repository import UserRepository
from src.repositories.system_repository import SystemRepository
from src.repositories.system_log_repository import SystemLogRepository
from src.bot.constants import STAT_CHAT_ID, JOIN_THREAD_ID, USER_LOG_THREAD_ID


async def stat_task(stat_bot: Bot, session_factory: async_sessionmaker[AsyncSession]) -> None:
    while True:
        
        session = session_factory()
        user_repository = UserRepository(session)
        system_repository = SystemRepository(session)
        system_log_repository = SystemLogRepository(session)
        try:
            async with session.begin():
                system = await system_repository.get()
                all_u = await user_repository.get_users_order_by_join_and_limit(system.last_user_log, system.max_user_cumulative)
                all_logs = await system_log_repository.get_logs_order_by_time_and_limit(system.last_action_log, system.max_user_cumulative)

                if all_u:
                    system.last_user_log = all_u[-1].created_at

                if all_logs:
                    system.last_action_log = all_logs[-1].created_at

                if all_u or all_logs:
                    await system_repository.update(system)            
            if all_u:
                text = "\n\n".join([f"{i+1}. {user.full_info}" for i, user in enumerate(all_u)])
                try:
                    await stat_bot.send_message(chat_id=STAT_CHAT_ID, message_thread_id=JOIN_THREAD_ID, text=text)
                except Exception as e:
                    print(e)

            if all_logs:
                text = "\n\n".join([f"{i+1}. {log.created_at}\nc: {log.command}\n {log.user.info}" for i, log in enumerate(all_logs)])
                try:
                    await stat_bot.send_message(chat_id=STAT_CHAT_ID, message_thread_id=USER_LOG_THREAD_ID, text=text)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e) # todo send to system log
        finally:
            await session.close()
        await asyncio.sleep(60)