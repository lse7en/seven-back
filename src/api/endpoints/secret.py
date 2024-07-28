
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from src.deps import  CurrentUserId
from src.core.database import DBSession
from src.schemas.user_schemas import User
import random
from datetime import datetime, UTC, timedelta, date, time
from src.repositories.user_repository import UserRepository
from src.repositories.system_log_repository import SystemLogRepository
from src.models.system_log import SystemLog
from src.core.schema import BaseModel


router = APIRouter(prefix="/secret", tags=["secret"])

# utc date to secret
SECRETS = {

    "2024-07-23": "reduce",
    "2024-07-24": "reduce",
    "2024-07-25": "tickets",
    "2024-07-26": "tomorrow",
    "2024-07-27": "the charm",
    "2024-07-28": "august 7",
    
}

#body
class SecretRequest(BaseModel):
    secret: str



def get_secret_reset_datetime(date: date):
    # create a date time in utc timezone with the given date and time 16:00:00
    return datetime.combine(date, time(16, 0, 0), tzinfo=UTC) + timedelta(days=1)

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
    system_log_repository: Annotated[SystemLogRepository, Depends()]
):
    
    secret = secret_request.secret



    async with session.begin():
        user = await user_repository.get_user_for_update(user_id)


        if datetime.now(UTC) < get_secret_reset_datetime(user.last_secret_code_date):
            return user
        
        key = get_now_key()

        if secret.lower() == SECRETS.get(str(key), ""):
            await system_log_repository.add_log(SystemLog(user=user, command=f"🔵 secret 🔵:{secret} {user.points} -> {user.points + 1000}"))
            user.points += 1000
            user.last_secret_code_date = key
            await user_repository.add_user(user)
            return user
        else:
            raise HTTPException(status_code=400, detail="invalid_secret_code")