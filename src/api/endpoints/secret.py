
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from src.deps import  CurrentUserId
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
    "2024-07-03": "invite",
    "2024-07-04": "jackpot",
    "2024-07-05": "airdrop",
    "2024-07-06": "ticket",
}

#body
class SecretRequest(BaseModel):
    secret: str


@router.post("", response_model=User)
async def secret(
    user_id: CurrentUserId,
    secret_request: SecretRequest,
    session: DBSession,
    user_repository: Annotated[UserRepository, Depends()],
    system_log_repository: Annotated[SystemLogRepository, Depends()]
):
    
    secret = secret_request.secret

    current_date = datetime.now(UTC).date()


    async with session.begin():
        user = await user_repository.get_user_for_update(user_id)


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