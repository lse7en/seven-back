
from typing import Annotated
from fastapi import APIRouter, Depends, Request

from src.deps import  CurrentUser
from src.schemas.user_schemas import User, UserBase
from src.repositories.user_repository import UserRepository
from src.bot.validators import is_member_of
from src.bot.constants import COMMUNITY_TID
router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", response_model=User)
async def profile(
    current_user: CurrentUser
):
    return current_user


@router.get("/friends", response_model=list[UserBase])
async def friends(
    current_user: CurrentUser,
    user_repository: Annotated[UserRepository, Depends()]

):
    friends = await user_repository.get_friends(current_user.id)
    return friends


@router.f ("/joined", response_model=User)
async def joined(
    request: Request,
    current_user: CurrentUser,
    user_repository: Annotated[UserRepository, Depends()]
):
    bot = request.app.state.stat_bot
    current_user.joined = await is_member_of(bot, COMMUNITY_TID, current_user.id)
    await user_repository.add_user(current_user)
    return current_user