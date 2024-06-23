
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from src.deps import  CurrentUser
from src.core.database import DBSession
from src.schemas.user_schemas import User
import random
from datetime import datetime, UTC, timedelta
from src.repositories.user_repository import UserRepository
from src.repositories.system_log_repository import SystemLogRepository
from src.models.system_log import SystemLog
from src.core.schema import BaseModel


router = APIRouter(prefix="/secret", tags=["secret"])

# utc date to secret
SECRETS = {
    "2024-06-22": "start",
    "2024-06-23": "start",
    "2024-06-24": "community",
    "2024-06-25": "lucky",
    "2024-06-26": "ton",
    "2024-06-27": "telegram",
    "2024-06-28": "dao",
    "2024-06-29": "crypto",
    "2024-06-30": "l7",


}

#body
class SecretRequest(BaseModel):
    secret: str


@router.post("", response_model=User)
async def secret(
    current_user: CurrentUser,
    secret_request: SecretRequest,
    session: DBSession,
    user_repository: Annotated[UserRepository, Depends()],
    system_log_repository: Annotated[SystemLogRepository, Depends()]
):
    
    secret = secret_request.secret

    current_date = datetime.now(UTC).date()


    # generate random  between 1 and 20
    u_id = current_user.id

    async with session.begin():
        user = await user_repository.get_user_for_update(u_id)


        if user.last_secret_code_date == current_date:
            return user
        
        if secret.lower() == SECRETS.get(str(current_date), ""):
            await system_log_repository.add_log(SystemLog(user=user, command=f"secret:{secret} {user.points} -> {user.points + 500}"))
            user.points += 500
            user.last_secret_code_date = current_date
            await user_repository.add_user(user)
            return user
        else:
            raise HTTPException(status_code=400, detail="invalid_secret_code")