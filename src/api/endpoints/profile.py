
from typing import Annotated
from fastapi import APIRouter, Depends

from src.deps import  CurrentUser
from src.schemas.user_schemas import User, UserBase
from src.repositories.user_repository import UserRepository
router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", response_model=User)
async def profile(
    current_user: CurrentUser,
    user_repository: Annotated[UserRepository, Depends()]

):
    return current_user


@router.get("/friends", response_model=[UserBase])
async def friends(
    current_user: CurrentUser,
    user_repository: Annotated[UserRepository, Depends()]

):
    friends = await user_repository.get_friends(current_user.id)
    return friends