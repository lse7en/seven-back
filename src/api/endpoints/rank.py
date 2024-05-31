
from typing import Annotated
from fastapi import APIRouter, Depends

from src.deps import  CurrentUser
from src.core.database import DBSession
from src.schemas.user_schemas import User
import random
from src.repositories.user_repository import UserRepository
router = APIRouter(prefix="/rank", tags=["rank"])


@router.get("", response_model=User)
async def rank(
    current_user: CurrentUser,
    user_repository: Annotated[UserRepository, Depends()]
):
    rank = await user_repository.get_user_rank(current_user.id)
    current_user.rank = rank

    return current_user