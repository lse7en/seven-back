
from typing import Annotated
from fastapi import APIRouter, Depends

from src.deps import  CurrentUser
from src.core.database import DBSession
from src.schemas.user_schemas import User
import random
from datetime import datetime, UTC, timedelta
from src.repositories.user_repository import UserRepository
from src.repositories.system_log_repository import SystemLogRepository
from src.models.system_log import SystemLog
from
router = APIRouter(prefix="/lpush", tags=["lpush"])


@router.post("", response_model=User)
async def lpush(
    current_user: CurrentUser,
    session: DBSession,
    user_repository: Annotated[UserRepository, Depends()],
    system_log_repository: Annotated[SystemLogRepository, Depends()]
):
    # generate random  between 1 and 20
    r = random.randint(1, 200)


    minutes = (2 ** (3 - current_user.invited_users)) * 60

    next_push = current_user.last_lucky_push + timedelta(minutes=minutes)

    if datetime.now(UTC) < next_push:
        return current_user

    async with session.begin():
        await system_log_repository.add_log(SystemLog(user=current_user, command="get:push"))
        current_user.push_points += r
        current_user.points += r
        current_user.last_lucky_push = datetime.now(UTC)
        await user_repository.add_user(current_user)

    return current_user