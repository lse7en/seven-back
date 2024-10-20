from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from src.deps import CurrentUserId
from src.core.database import DBSession
from src.schemas.user_schemas import User
from datetime import datetime, UTC, timedelta
from src.repositories.user_repository import UserRepository
from src.repositories.system_log_repository import SystemLogRepository
from src.repositories.secret_repository import SecretCodeRepository
from src.models.system_log import SystemLog, LogTag
from src.core.schema import BaseModel
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
):
    secret = secret_request.secret.lower().strip()

    async with session.begin():
        user = await user_repository.get_user_for_update(user_id)

        if datetime.now(UTC) < user.secret_reset_datetime:
            return user

        key = get_now_key()

        if await secret_code_repository.exists(key, secret):
            await system_log_repository.add_log(
                SystemLog(
                    user=user,
                    command=f"🔵 secret 🔵:{secret} {user.points} -> {user.points + ActionPoints.SECRET}",
                    tag=LogTag.SECRET,
                )
            )
            user.points += ActionPoints.SECRET
            user.last_secret_code_date = key
            await user_repository.add_user(user)
            return user
        else:
            raise HTTPException(status_code=400, detail="invalid_secret_code")
