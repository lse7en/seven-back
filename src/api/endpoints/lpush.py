
from typing import Annotated
from fastapi import APIRouter, Depends

from src.deps import  CurrentUser
from src.core.database import DBSession
from src.schemas.user_schemas import User
import random
from src.repositories.user_repository import UserRepository
router = APIRouter(prefix="/lpush", tags=["lpush"])


@router.post("", response_model=User)
async def lpush(
    current_user: CurrentUser,
    session: DBSession,
    user_repository: Annotated[UserRepository, Depends()]
):
    # generate random  between 1 and 20
    r = random.randint(1, 20)

    async with session.begin():
        current_user.lucky_points += r/100
        await user_repository.add_user(current_user)

    return current_user