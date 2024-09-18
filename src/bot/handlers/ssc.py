from aiogram.types import Message

from datetime import datetime, UTC, timedelta
from aiogram.filters import CommandObject

from src.models.secret import SecretCode
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.bot import beans
from src.bot.permissions import HasPermissions



def get_now_key():
    now = datetime.now(UTC)

    if now.hour < 16:
        return (now - timedelta(days=1)).date()
    else:
        return now.date()

@HasPermissions(1)
async def ssc_handler(
    message: Message,
    command: CommandObject,
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    
    session = session_factory()
    secret_code_repository = await beans.get_secret_code_repository(session)

    try:
        parts = (command.args if command.args else "").lower().split()

        if len(parts) < 2:

            now_key = get_now_key()

            async with session.begin():
                current_secret = await secret_code_repository.get_by_key(now_key)

            if current_secret is None:
                await message.answer(f"No secret for key {now_key}")
            else:
                await message.answer(f"Current secret: key: {current_secret.key}, secret: {current_secret.secret}")
            return
        
        key = datetime.strptime(parts[0], "%Y-%m-%d").date()
        secret = ' '.join(parts[1:])

        try:
            async with session.begin():
                sc = SecretCode(key=key, secret=secret)
                await secret_code_repository.add(sc)
        except Exception as e:
            await message.answer("Error: on setting")
            return

        await message.answer(f"Secret code added: '{key}': '{secret}'")
    except Exception as e:
        await message.answer(f"Error: {e}")
    
