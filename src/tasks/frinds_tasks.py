from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.models.enums import FriendsTask, TaskStatus
from src.models.user import User
from src.models.lottery import Ticket
from sqlalchemy import update, select
from sqlalchemy.sql.functions import count



async def friend_extra_check(
    session_factory: async_sessionmaker[AsyncSession],
    user_id: int,
    current_status: TaskStatus,
    task: FriendsTask,
) -> None:
    
    if current_status != TaskStatus.NOT_DONE:
        return


    session = session_factory()


    if task == FriendsTask.SECRET_CODE:
        query = update(User).where(User.id == user_id, User.tasks_secret_code == TaskStatus.NOT_DONE).values(tasks_secret_code=TaskStatus.DONE)
    elif task == FriendsTask.WATCH_ADS:
        query = update(User).where(User.id == user_id, User.tasks_watch_ads == TaskStatus.NOT_DONE).values(tasks_watch_ads=TaskStatus.DONE)
    elif task == FriendsTask.ACTIVE_TICKETS:
        active_tickets_subquery = select(count(Ticket.id)).where(Ticket.user_id == user_id).scalar_subquery()
        query = update(User).where(User.id == user_id, User.tasks_active_tickets == TaskStatus.NOT_DONE).where(active_tickets_subquery > 9).values(tasks_active_tickets=TaskStatus.DONE)
    
    elif task == FriendsTask.JOIN_CHANNEL:
        query = update(User).where(User.id == user_id, User.tasks_join_channel == TaskStatus.NOT_DONE).where(User.joined == True).values(tasks_join_channel=TaskStatus.DONE)
    
    elif task == FriendsTask.REFER_A_FRIEND:
        query = update(User).where(User.id == user_id, User.tasks_refer_a_friend == TaskStatus.NOT_DONE).values(tasks_refer_a_friend=TaskStatus.DONE)
    else:
        print("Unknown task")

    async with session.begin():
        await session.execute(query)
