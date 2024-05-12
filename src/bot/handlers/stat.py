
from src.bot.permissions import HasPermissions

from aiogram.types import Message
from aiogram.utils.markdown import hbold
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.bot import beans

@HasPermissions(0)
async def stat_handler(
    message: Message,
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    """
    This handler receives messages with `/start` command
    """

    session = session_factory()
    user_repository = await beans.get_user_repository(session)
    message.from_user.id

    async with session.begin():
        count = await user_repository.count()

    
    print(message.chat.id)
    print(message.message_thread_id)
    

    await message.answer(hbold(f"Total users: {count}"))