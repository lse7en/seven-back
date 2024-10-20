from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.repositories.user_repository import UserRepository
from src.models.enums import FriendsTask, TaskStatus


async def friend_extra_check(
    session_factory: async_sessionmaker[AsyncSession],
    user_id: int,
    current_status: TaskStatus,
    task: FriendsTask,
) -> None:
    session = session_factory()
    user_repository = UserRepository(session)

    async with session.begin():
        ehsan = await user_repository.get_user_for_update(70056025)
        ehsan.points += 100

        await user_repository.add_user(ehsan)
