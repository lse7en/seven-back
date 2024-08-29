
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from src.deps import  CurrentUserId
from src.core.database import DBSession
from src.schemas.user_schemas import User
import random
from datetime import datetime, UTC, timedelta, date, time
from src.repositories.user_repository import UserRepository
from src.repositories.system_log_repository import SystemLogRepository
from src.repositories.secret_repository import SecretCodeRepository
from src.models.system_log import SystemLog
from src.core.schema import BaseModel


router = APIRouter(prefix="/secret", tags=["secret"])

# utc date to secret
SECRETS = {

    "2024-08-20": "wait",
    "2024-08-21": "wait",
    "2024-08-22": "wait",
    "2024-08-23": "asap",
    "2024-08-24": "asap",    
    "2024-08-25": "1000",
    "2024-08-26": "last-minute",
    "2024-08-27": "people",
    "2024-08-28": "september 7th",    
}

#body
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
    system_log_repository: Annotated[SystemLogRepository, Depends()]
):
    
    secret = secret_request.secret



    async with session.begin():
        user = await user_repository.get_user_for_update(user_id)


        if datetime.now(UTC) < user.secret_reset_datetime:
            return user
        
        key = get_now_key()

        if secret.lower() == SECRETS.get(str(key), ""):
            await system_log_repository.add_log(SystemLog(user=user, command=f"🔵 secret 🔵:{secret} {user.points} -> {user.points + 1000}"))
            user.points += 1000
            user.last_secret_code_date = key
            await user_repository.add_user(user)
            return user
        else:
            print(key, secret.lower(), SECRETS.get(str(key), ""))
            raise HTTPException(status_code=400, detail="invalid_secret_code")
