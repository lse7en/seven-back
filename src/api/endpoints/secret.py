
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
    "2024-07-29": "whatever",
    "2024-07-30": "whatever",
    "2024-07-31": "boost",
    "2024-08-01": "premium",
    "2024-08-02": "premium",
    "2024-08-03": "unchain",
    "2024-08-04": "surprise",
    "2024-08-05": "pot",
    "2024-08-06": "august",
    "2024-08-07": "easy",
    "2024-08-08": "find",
    "2024-08-09": "find",
    "2024-08-10": "friend",
    "2024-08-11": "a lot",
    "2024-08-12": "party",
    "2024-08-13": "sleeping",
    "2024-08-14": "sleeping",
    "2024-08-15": "jackpot",
    "2024-08-16": "jackpot",
    "2024-08-17": "august 27",
    "2024-08-18": "august 27",
    "2024-08-19": "august 27",
    "2024-08-20": "wait"
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
