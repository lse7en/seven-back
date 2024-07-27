
from typing import Annotated
from fastapi import APIRouter, Depends

from src.deps import  CurrentUserId
from src.core.database import DBSession
from src.schemas.user_schemas import User
from datetime import datetime, UTC, timedelta
from src.repositories.user_repository import UserRepository
from src.repositories.system_log_repository import SystemLogRepository
from src.models.system_log import SystemLog
router = APIRouter(prefix="/adsg", tags=["adsg"])


@router.post("", response_model=User)
async def reduce_time(
    user_id: CurrentUserId,
    session: DBSession,
    user_repository: Annotated[UserRepository, Depends()],
    system_log_repository: Annotated[SystemLogRepository, Depends()]
):


    async with session.begin():   
        user = await user_repository.get_user_for_update(user_id)


        
        if user.ads_reduce_time == 0:
            return user
        
        rt = user.ads_reduce_time
        user.last_lucky_push = user.last_lucky_push - timedelta(minutes=rt)

        user.total_ads_watched_this_push += 1
        user.total_ads_watched += 1

        await system_log_repository.add_log(SystemLog(user=user, command=f"🟡 ads 🟡: {user.total_ads_watched_this_push}, {rt}"))

        await user_repository.add_user(user)

        return user


@router.post("/point", response_model=User)
async def ad_point(
    user_id: CurrentUserId,
    session: DBSession,
    user_repository: Annotated[UserRepository, Depends()],
    system_log_repository: Annotated[SystemLogRepository, Depends()]
):


    async with session.begin():   
        user = await user_repository.get_user_for_update(user_id)



        if datetime.now(UTC) < user.next_ad_for_points:
            return user
        

        user.last_ads_watch_for_points = datetime.now(UTC)
        user.points += 100
        user.total_ads_watched_for_points += 1

        await system_log_repository.add_log(SystemLog(user=user, command=f"⚫ ads ⚫: {user.total_ads_watched_for_points}"))

        await user_repository.add_user(user)

        return user