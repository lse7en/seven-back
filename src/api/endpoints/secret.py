from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from src.deps import CurrentUserId
from src.core.database import DBSession
from src.schemas.user_schemas import User
from datetime import datetime, UTC, timedelta
from src.repositories.user_repository import UserRepository
from src.repositories.system_log_repository import SystemLogRepository
from src.repositories.secret_repository import SecretCodeRepository
from src.models.system_log import SystemLog
from src.models.enums import LogTag, FriendsTask
from src.core.schema import BaseModel
from src.tasks.bg import BackgroundTasksWrapper
from src.constants import ActionPoints

router = APIRouter(prefix="/secret", tags=["secret"])


# body
class SecretRequest(BaseModel):
    secret: str


def get_now_key():
    now = datetime.now(UTC)

    if now.hour < 16:
        return (now - timedelta(days=1)).date()
    else:
        return now.date()


@router.post("", response_model=User)
async def secret(
    user_id: CurrentUserId,
    secret_request: SecretRequest,
    session: DBSession,
    user_repository: Annotated[UserRepository, Depends()],
    secret_code_repository: Annotated[SecretCodeRepository, Depends()],
    system_log_repository: Annotated[SystemLogRepository, Depends()],
    background_tasks: Annotated[BackgroundTasksWrapper, Depends()],
):
    secret = secret_request.secret.lower().strip()

    async with session.begin():
        user = await user_repository.get_user_for_update(user_id)

        if datetime.now(UTC) < user.secret_reset_datetime:
            return user

        key = get_now_key()

        if not await secret_code_repository.exists(key, secret):
            raise HTTPException(status_code=400, detail="invalid_secret_code")
        
        user.points += ActionPoints.SECRET.value
        user.last_secret_code_date = key
        await user_repository.add_user(user)
        background_tasks.friend_extra_check(user_id=user_id, current_status=user.tasks_secret_code, task=FriendsTask.SECRET_CODE)
        background_tasks.save_log(user_id=user_id, command=f"{user.points} -> {user.points + ActionPoints.SECRET.value}", tag=LogTag.SECRET)

        return user

