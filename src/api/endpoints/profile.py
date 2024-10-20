
from typing import Annotated
from fastapi import APIRouter, Depends, Request

from src.deps import CurrentUserId
from src.schemas.user_schemas import User, UserFriend
from src.repositories.user_repository import UserRepository
from src.repositories.lottery_repository import TicketRepository
from src.bot.validators import is_member_of
from src.bot.constants import COMMUNITY_TID
from src.models.enums import FriendsTask
from src.tasks.bg import BackgroundTasksWrapper
from src.constants import ActionPoints
router = APIRouter(prefix="/profile", tags=["profile"])

@router.get("", response_model=User)
async def profile(
    user_id: CurrentUserId,
    user_repository: Annotated[UserRepository, Depends()],
):
    return await user_repository.get_user_or_none_by_id(user_id)


@router.get("/friends", response_model=list[UserFriend])
async def friends(
    user_id: CurrentUserId,
    user_repository: Annotated[UserRepository, Depends()],
    ticket_repository: Annotated[TicketRepository, Depends()],

):
    friends = await user_repository.get_friends(user_id)

    friends_with_todo_active_ticket_tasks = [friend.id for friend in friends if friend.tasks_active_tickets.is_todo()]

    friend_id_to_ticket_count = await ticket_repository.get_ticket_count_for_users(friends_with_todo_active_ticket_tasks)

    for friend in friends:
        friend.active_tickets_count = min(friend_id_to_ticket_count.get(friend.id, 10), 10)

    return friends


@router.post("/joined", response_model=User)
async def joined(
    request: Request,
    user_id: CurrentUserId,
    user_repository: Annotated[UserRepository, Depends()],
    background_tasks: Annotated[BackgroundTasksWrapper, Depends()],
):
    bot = request.app.state.bot
    joined = await is_member_of(bot, COMMUNITY_TID, user_id)

    # if not joined:
    #     return await user_repository.get_user_or_none_by_id(user_id)


    async with user_repository.session.begin():
        current_user = await user_repository.get_user_for_update(user_id)
        current_user.joined = joined

        if joined and not current_user.join_reward:
            current_user.points += ActionPoints.JOIN.value
            current_user.join_reward = True

        await user_repository.add_user(current_user)
        background_tasks.friend_extra_check(user_id=user_id, current_status=current_user.tasks_join_channel, task=FriendsTask.JOIN_CHANNEL)

    return current_user