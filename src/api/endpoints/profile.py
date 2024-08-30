
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

    # if not joined:
    #     return await user_repository.get_user_or_none_by_id(user_id)

    send_text_to_referrer = False

    async with user_repository.session.begin():
        current_user = await user_repository.get_user_for_update(user_id)
        current_user.joined = joined

        if joined and current_user.referrer_id and not current_user.referrer_score:
            referrer = await user_repository.get_user_for_update(current_user.referrer_id)
            referrer.invited_users += 1
            referrer.points += 1000
            await user_repository.add_user(referrer)

            current_user.referrer_score = True
            send_text_to_referrer = True

        if joined and not current_user.join_reward:
            current_user.points += 1000
            current_user.join_reward = True


        await user_repository.add_user(current_user)

    
    if send_text_to_referrer:
        joined_message = formatting.as_list(
            formatting.as_line(formatting.Bold(get_text(referrer.language, "Keep going!")), "💪", sep=" "),
            formatting.as_line(
                get_text(referrer.language, "Your friend"),
                formatting.Bold(current_user.full_name),
                get_text(referrer.language, "joined the Bot!"),
                sep=" ",
            ),
            formatting.as_list(
                get_text(referrer.language, "And You get 1000 points and 1 extra ticket for that!"),
            ),
            sep="\n\n",
        )
        try:
            await request.app.state.bot.send_photo(
                chat_id=referrer.id,
                photo=FRIEND_INVITE_FILE_ID,
                caption=joined_message.as_html(),
            )
        except Exception as e:
            print("kire kharg")
            print(e)


    return current_user