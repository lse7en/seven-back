
from typing import Annotated
from fastapi import APIRouter, Depends

from src.deps import  CurrentUser
from src.core.database import DBSession
from src.schemas.user_schemas import Rank
import random
from src.repositories.user_repository import UserRepository
router = APIRouter(prefix="/rank", tags=["rank"])


@router.get("", response_model=Rank)
async def rank(
    current_user: CurrentUser,
    session: DBSession,
    user_repository: Annotated[UserRepository, Depends()]
):
    rank = await user_repository.get_user_rank(current_user.id)

    return Rank(rank=rank)