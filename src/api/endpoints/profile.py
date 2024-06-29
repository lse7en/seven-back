
from typing import Annotated
from fastapi import APIRouter, Depends, Request

from src.deps import CurrentUserId
from src.schemas.user_schemas import User, UserBase
from src.repositories.user_repository import UserRepository
from src.bot.validators import is_member_of
from src.bot.constants import COMMUNITY_TID, FRIEND_INVITE_FILE_ID
from src.bot.text import get_text
from aiogram.utils import formatting
router = APIRouter(prefix="/profile", tags=["profile"])

@router.get("", response_model=User)
async def profile(
    user_id: CurrentUserId,
    user_repository: Annotated[UserRepository, Depends()],
):
    return await user_repository.get_user_or_none_by_id(user_id)


@router.get("/friends", response_model=list[UserBase])
async def friends(
    user_id: CurrentUserId,
    user_repository: Annotated[UserRepository, Depends()],

):
    friends = await user_repository.get_friends(user_id)
    return friends


@router.post("/joined", response_model=User)
async def joined(
    request: Request,
    user_id: CurrentUserId,
    user_repository: Annotated[UserRepository, Depends()],
):
    bot = request.app.state.bot
    joined = await is_member_of(bot, COMMUNITY_TID, user_id)

    if not joined:
        return await user_repository.get_user_or_none_by_id(user_id)


    async with user_repository.session.begin():
        current_user = await user_repository.get_user_for_update(user_id)
        current_user.joined = joined

        if joined and current_user.referrer_id and not current_user.referrer_score:
            referrer = await user_repository.get_user_for_update(current_user.referrer_id)
            referrer.invited_users += 1
            referrer.points += 1000
            await user_repository.add_user(referrer)

            current_user.referrer_score = True


        await user_repository.add_user(current_user)

    


    return current_user