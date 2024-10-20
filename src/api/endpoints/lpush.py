
from typing import Annotated
from fastapi import APIRouter, Depends

from src.deps import  CurrentUserId
from src.tasks.bg import BackgroundTasksWrapper
from src.core.database import DBSession
from src.schemas.user_schemas import User
from datetime import datetime, UTC
from src.repositories.user_repository import UserRepository
from src.models.enums import LogTag
from src.constants import ActionPoints
router = APIRouter(prefix="/lpush", tags=["lpush"])


@router.post("", response_model=User)
async def lpush(
    user_id: CurrentUserId,
    session: DBSession,
    user_repository: Annotated[UserRepository, Depends()],
    background_tasks: Annotated[BackgroundTasksWrapper, Depends()]
):
    # generate random  between 1 and 20
    r = ActionPoints.PUSH.value


    async with session.begin():   
        user = await user_repository.get_user_for_update(user_id)



        if datetime.now(UTC) < user.next_push_time:
            return user
    
    
        background_tasks.save_log(user_id=user_id, command=f"{user.points} + {r} -> {user.points + r}", tag=LogTag.PUSH)
        user.push_points += r
        user.points += r
        user.push_count += 1
        user.last_lucky_push = datetime.now(UTC)
        user.total_ads_watched_this_push = 0
        await user_repository.add_user(user)

        return user
    