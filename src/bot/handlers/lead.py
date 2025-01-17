from aiogram.types import Message
from aiogram.filters import CommandObject

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.bot import beans
from src.bot.permissions import HasPermissions

@HasPermissions(2)
async def lead_handler(
    message: Message,
    command: CommandObject,
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    session = session_factory()
    user_repository = await beans.get_user_repository(session)

    try:
        lead = int(command.args) if command.args else 10
    except Exception as e:
        lead = 10

    if lead > 40:
        lead = 40

    async with session.begin():
        ids = await user_repository.get_users_with_ranking(lead)
        users = await user_repository.get_users_with_ids_in(ids)
        users = sorted(users, key=lambda x: ids.index(x.id))

        text = "\n\n".join(
            [
                f"{i+1}. {user.info}"
                for i, user in enumerate(users)
            ]
        )

    await message.answer(text)
