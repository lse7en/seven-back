from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import computed_field
from src.core.schema import BaseModel
from src.models.enums import FriendsTask, TaskStatus, LogTag
from src.deps import CurrentUserId
from src.repositories.user_repository import UserRepository
from src.constants import ActionPoints
from src.tasks.bg import BackgroundTasksWrapper

router = APIRouter(prefix="/tasks/friends", tags=["tasks_friends"])



# body
class ClaimRequest(BaseModel):
    friend_id: int
    task: FriendsTask


class ClaimResponse(ClaimRequest):
    new_points: int
    new_tickets: int

    #tasks info
    tasks_join_channel: TaskStatus
    tasks_active_tickets: TaskStatus
    tasks_refer_a_friend: TaskStatus
    tasks_secret_code: TaskStatus
    tasks_watch_ads: TaskStatus



    @computed_field
    @property
    def number_of_done_tasks(self) -> int:
        return sum([
            self.tasks_join_channel == TaskStatus.CLAIMED,
            self.tasks_active_tickets == TaskStatus.CLAIMED,
            self.tasks_refer_a_friend == TaskStatus.CLAIMED,
            self.tasks_secret_code == TaskStatus.CLAIMED,
            self.tasks_watch_ads == TaskStatus.CLAIMED,
        ])



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
            background_tasks.save_log(user_id=user_id, command=f"{claim_request.task.value}", tag=LogTag.CLAIM.value)


    return ClaimResponse(friend_id=claim_request.friend_id, task=claim_request.task, new_points=user.points, new_tickets=user.invited_users + 1).model_dump()