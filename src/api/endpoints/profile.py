
from typing import Annotated
from fastapi import APIRouter, Depends

from src.deps import  CurrentUser
from src.schemas.user_schemas import User
from src.repositories.user_repository import UserRepository
router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", response_model=User)
async def profile(
    current_user: CurrentUser,
    user_repository: Annotated[UserRepository, Depends()]

):
    friends = await UserRepository.get_friends(current_user.id)
    current_user.friends = friends
    return current_user