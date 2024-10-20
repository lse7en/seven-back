from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from src.core.schema import BaseModel
from src.models.enums import FriendsTask, TaskStatus, LogTag
from src.deps import CurrentUserId
from src.repositories.user_repository import UserRepository
from src.constants import ActionPoints
from src.tasks.bg import BackgroundTasksWrapper
from src.schemas.user_schemas import UserFriend

router = APIRouter(prefix="/tasks/friends", tags=["tasks_friends"])


# body
class ClaimRequest(BaseModel):
    friend_id: int
    task: FriendsTask


class ClaimResponse(ClaimRequest):
    new_points: int
    new_tickets: int

    friend: UserFriend



def get_first_task(user):
    if user.tasks_watch_ads == TaskStatus.DONE:
        return FriendsTask.WATCH_ADS
    if user.tasks_secret_code == TaskStatus.DONE:
        return FriendsTask.SECRET_CODE
    if user.tasks_refer_a_friend == TaskStatus.DONE:
        return FriendsTask.REFER_A_FRIEND
    if user.tasks_active_tickets == TaskStatus.DONE:
        return FriendsTask.ACTIVE_TICKETS
    if user.tasks_join_channel == TaskStatus.DONE:
        return FriendsTask.JOIN_CHANNEL
    
    if user.tasks_watch_ads == TaskStatus.NOT_DONE:
        return FriendsTask.WATCH_ADS
    if user.tasks_secret_code == TaskStatus.NOT_DONE:
        return FriendsTask.SECRET_CODE
    if user.tasks_refer_a_friend == TaskStatus.NOT_DONE:
        return FriendsTask.REFER_A_FRIEND
    if user.tasks_active_tickets == TaskStatus.NOT_DONE:
        return FriendsTask.ACTIVE_TICKETS
    if user.tasks_join_channel == TaskStatus.NOT_DONE:
        return FriendsTask.JOIN_CHANNEL
    

    return None



@router.get("/nexts", response_model=list[ClaimResponse])
async def next_task(
    user_id: CurrentUserId,
    user_repository: Annotated[UserRepository, Depends()],
):
    
    total_tasks = 2
    user = await user_repository.get_user_or_none_by_id(user_id)


    friends = await user_repository.get_friends_with_task_status_and_limit(user_id, TaskStatus.DONE, total_tasks)


    if len(friends) < total_tasks:
        friends += await user_repository.get_friends_with_task_status_and_limit(user_id, TaskStatus.NOT_DONE, total_tasks - len(friends))

    
    res = []

    for friend in friends:
        friend.active_tickets_count = 0
        res.append(
            ClaimResponse(
                friend_id=friend.id,
                task=get_first_task(friend),
                new_points=user.points,
                new_tickets=user.invited_users + 1,
                friend=UserFriend.model_validate(friend, from_attributes=True),
            )
        )

    return res




@router.post("/claim")
async def claim(
    user_id: CurrentUserId,
    claim_request: ClaimRequest,
    user_repository: Annotated[UserRepository, Depends()],
    background_tasks: Annotated[BackgroundTasksWrapper, Depends()],
):
    async with user_repository.session.begin():
        friend = await user_repository.get_user_for_update(claim_request.friend_id)

        if not friend or friend.referrer_id != user_id:
            raise HTTPException(status_code=400, detail="invalid_friend_id")

        user = await user_repository.get_user_for_update(user_id)

        apply_claim = False

        if claim_request.task == FriendsTask.WATCH_ADS:
            if friend.tasks_watch_ads == TaskStatus.DONE:
                friend.tasks_watch_ads = TaskStatus.CLAIMED
                user.points += ActionPoints.TASKS_WATCH_ADS.value
                apply_claim = True

        elif claim_request.task == FriendsTask.SECRET_CODE:
            if friend.tasks_secret_code == TaskStatus.DONE:
                friend.tasks_secret_code = TaskStatus.CLAIMED
                user.points += ActionPoints.TASKS_SECRET_CODE.value
                apply_claim = True

        elif claim_request.task == FriendsTask.REFER_A_FRIEND:
            if friend.tasks_refer_a_friend == TaskStatus.DONE:
                friend.tasks_refer_a_friend = TaskStatus.CLAIMED
                user.points += ActionPoints.TASKS_REFER_A_FRIEND.value
                apply_claim = True

        elif claim_request.task == FriendsTask.ACTIVE_TICKETS:
            if friend.tasks_active_tickets == TaskStatus.DONE:
                friend.tasks_active_tickets = TaskStatus.CLAIMED
                user.points += ActionPoints.TASKS_ACTIVE_TICKETS.value
                apply_claim = True

        elif claim_request.task == FriendsTask.JOIN_CHANNEL:
            if friend.tasks_join_channel == TaskStatus.DONE:
                friend.tasks_join_channel = TaskStatus.CLAIMED
                user.points += ActionPoints.TASKS_JOIN_CHANNEL.value
                user.invited_users += 1
                apply_claim = True

        else:
            raise HTTPException(status_code=400, detail="invalid_task")

        if apply_claim:
            await user_repository.add_user(user)
            await user_repository.add_user(friend)
            background_tasks.save_log(
                user_id=user_id, command=f"{claim_request.task.value}", tag=LogTag.CLAIM
            )

    friend.active_tickets_count = 0
    friend_dump = UserFriend.model_validate(friend, from_attributes=True)
    return ClaimResponse(
        friend_id=claim_request.friend_id,
        task=claim_request.task,
        new_points=user.points,
        new_tickets=user.invited_users + 1,
        friend=friend_dump,
    )

