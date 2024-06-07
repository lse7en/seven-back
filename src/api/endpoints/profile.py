
from typing import Annotated
from fastapi import APIRouter, Depends, Request

from src.deps import  CurrentUser
from src.schemas.user_schemas import User, UserBase
from src.repositories.user_repository import UserRepository
from src.repositories.system_log_repository import SystemLogRepository
from src.models.system_log import SystemLog
from src.bot.validators import is_member_of
from src.bot.constants import COMMUNITY_TID
from src.bot.text import get_text
from aiogram.utils import formatting
router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", response_model=User)
async def profile(
    current_user: CurrentUser,
    system_log_repository: Annotated[SystemLogRepository, Depends()]
):
    await system_log_repository.add_log(SystemLog(user=current_user, command="get:profile"))
    return current_user


@router.get("/friends", response_model=list[UserBase])
async def friends(
    current_user: CurrentUser,
    user_repository: Annotated[UserRepository, Depends()]

):
    friends = await user_repository.get_friends(current_user.id)
    return friends


@router.post("/joined", response_model=User)
async def joined(
    request: Request,
    current_user: CurrentUser,
    user_repository: Annotated[UserRepository, Depends()]
):
    bot = request.app.state.stat_bot
    current_user.joined = await is_member_of(bot, COMMUNITY_TID, current_user.id)
    async with user_repository.session.begin():
        await user_repository.add_user(current_user)


    if current_user.joined and current_user.referrer_id and not current_user.referrer_score:
        referrer = await user_repository.get_user_or_none_by_id(current_user.referrer_id)

        async with user_repository.session.begin():
            referrer.invited_users += 1
            referrer.points += 1000
            await user_repository.add_user(referrer)


        joined_message = formatting.as_list(
            formatting.as_line(formatting.Bold(get_text(referrer.language, "Keep going!")), "💪", sep=" "),
            formatting.as_line(
                get_text(referrer.language, "Your friend"),
                formatting.Bold(current_user.full_name),
                get_text(referrer.language, "joined the Bot!"),
                sep=" ",
            ),
            formatting.as_list(
                get_text(referrer.language, "And You get 1000 points for that!"),
            )
            ,
            formatting.as_list(
                get_text(referrer.language, "You have invited {} friends.").format(referrer.invited_users),
                formatting.as_line(
                    get_text(referrer.language, "And you have gathered"),
                    formatting.Italic(f"{referrer.points}"),
                    get_text(referrer.language, "points so far!"),
                    sep=" ",
                ),
            ),
            sep="\n\n",
        )

        await request.app.state.bot.send_message(
            chat_id=referrer.id,
            **joined_message.as_kwargs(),
        )

    return current_user