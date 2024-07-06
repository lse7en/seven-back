
from typing import Annotated
from fastapi import APIRouter, Depends

from src.deps import  CurrentUserId
from src.core.database import DBSession
from src.schemas.user_schemas import User
import random
from datetime import datetime, UTC, timedelta
from src.repositories.user_repository import UserRepository
from src.repositories.system_log_repository import SystemLogRepository
from src.models.system_log import SystemLog
router = APIRouter(prefix="/lpush", tags=["lpush"])


@router.post("", response_model=User)
async def lpush(
    user_id: CurrentUserId,
    session: DBSession,
    user_repository: Annotated[UserRepository, Depends()],
    system_log_repository: Annotated[SystemLogRepository, Depends()]
):
    # generate random  between 1 and 20
    r = 250 #int(random.uniform(150.0, 300.0))

    async with session.begin():   
        user = await user_repository.get_user_for_update(user_id)


        minutes = (2 ** (3 - min(4, user.invited_users))) * 60

        next_push = user.last_lucky_push + timedelta(minutes=minutes)

        nn = datetime.now(UTC)

        if nn < next_push:
            return user
    
    
        await system_log_repository.add_log(SystemLog(user=user, command=f"🔴 push 🔴: {user.points} + {r} -> {user.points + r}"))
        user.push_points += r
        user.points += r
        user.last_lucky_push = datetime.now(UTC)
        await user_repository.add_user(user)

        return user
    