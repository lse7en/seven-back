
from typing import Annotated
from fastapi import APIRouter, Depends

from src.deps import  CurrentUserId
from src.core.database import DBSession
from src.schemas.user_schemas import User
from datetime import datetime, UTC
from src.repositories.user_repository import UserRepository
from src.repositories.system_log_repository import SystemLogRepository
from src.models.system_log import SystemLog, LogTag
from src.constants import ActionPoints
router = APIRouter(prefix="/lpush", tags=["lpush"])


@router.post("", response_model=User)
async def lpush(
    user_id: CurrentUserId,
    session: DBSession,
    user_repository: Annotated[UserRepository, Depends()],
    system_log_repository: Annotated[SystemLogRepository, Depends()]
):
    # generate random  between 1 and 20
    r = ActionPoints.PUSH


    async with session.begin():   
        user = await user_repository.get_user_for_update(user_id)



        if datetime.now(UTC) < user.next_push_time:
            return user
    
    
        await system_log_repository.add_log(SystemLog(user=user, command=f"🔴 push 🔴: {user.points} + {r} -> {user.points + r}", tag=LogTag.PUSH))
        user.push_points += r
        user.points += r
        user.push_count += 1
        user.last_lucky_push = datetime.now(UTC)
        user.total_ads_watched_this_push = 0
        await user_repository.add_user(user)

        return user
    