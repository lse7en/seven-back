
from typing import Annotated
from fastapi import APIRouter, Depends

from src.deps import  CurrentUserId
from src.tasks.bg import BackgroundTasksWrapper
from src.core.database import DBSession
from src.schemas.user_schemas import User
from datetime import datetime, UTC
from src.repositories.user_repository import UserRepository
from src.models.enums import LogTag, FriendsTask
from src.constants import ActionPoints
router = APIRouter(prefix="/adsg", tags=["adsg"])




@router.post("/point", response_model=User)
async def ad_point(
    user_id: CurrentUserId,
    session: DBSession,
    user_repository: Annotated[UserRepository, Depends()],
    background_tasks: Annotated[BackgroundTasksWrapper, Depends()]
):


    async with session.begin():   
        user = await user_repository.get_user_for_update(user_id)



        if datetime.now(UTC).timestamp() < user.next_ad_for_points.timestamp():
            return user
        

        user.last_ads_watch_for_points = datetime.now(UTC)
        user.points += ActionPoints.AD.value
        user.total_ads_watched_for_points += 1


        await user_repository.add_user(user)

        background_tasks.friend_extra_check(user_id=user_id, current_status=user.tasks_watch_ads, task=FriendsTask.WATCH_ADS)
        background_tasks.save_log(user_id=user_id, command=f"{user.total_ads_watched_for_points}", tag=LogTag.ADS_POINT)
        return user
    

@router.post("/double", response_model=User)
async def double_point(
    user_id: CurrentUserId,
    session: DBSession,
    user_repository: Annotated[UserRepository, Depends()],
    background_tasks: Annotated[BackgroundTasksWrapper, Depends()]
):


    async with session.begin():   
        user = await user_repository.get_user_for_update(user_id)
        

        user.last_ads_watch_for_points = datetime.now(UTC)
        user.points += ActionPoints.DOUBLE.value
        user.total_ads_watched_for_points += 1


        await user_repository.add_user(user)

        background_tasks.friend_extra_check(user_id=user_id, current_status=user.tasks_watch_ads, task=FriendsTask.WATCH_ADS)
        background_tasks.save_log(user_id=user_id, command=f"{user.total_ads_watched_for_points}", tag=LogTag.ADS_DOUBLE)

        return user