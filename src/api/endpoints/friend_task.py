from fastapi import APIRouter, Depends, Request, HTTPException
from src.core.schema import BaseModel
from src.models.enums import FriendsTask, TaskStatus
from src.deps import CurrentUserId
from src.repositories.user_repository import UserRepository
from src.constants import ActionPoints

router = APIRouter(prefix="/tasks/friends", tags=["tasks_friends"])



# body
class ClaimRequest(BaseModel):
    friend_id: int
    task: FriendsTask


class ClaimResponse(ClaimRequest):
    new_points: int
    new_tickets: int


@router.post("/claim", response_model=ClaimResponse)
async def claim(
    user_id: CurrentUserId,
    claim_request: ClaimRequest,
    user_repository: UserRepository,
):
    
    async with user_repository.session.begin():
        friend = await user_repository.get_user_for_update(claim_request.friend_id)

        if not friend or friend.referrer_id != user_id:
            raise HTTPException(status_code=400, detail="invalid_friend_id")

        user = await user_repository.get_user_for_update(user_id)

        if claim_request.task == FriendsTask.WATCH_ADS:
            if friend.tasks_watch_ads == TaskStatus.DONE:
                friend.tasks_watch_ads = TaskStatus.CLAIMED
                user.points += ActionPoints.TASKS_WATCH_ADS.value
        
        elif claim_request.task == FriendsTask.SECRET_CODE:
            if friend.tasks_secret_code == TaskStatus.DONE:
                friend.tasks_secret_code = TaskStatus.CLAIMED
                user.points += ActionPoints.TASKS_SECRET_CODE.value
        
        elif claim_request.task == FriendsTask.REFER_A_FRIEND:
            if friend.tasks_refer_a_friend == TaskStatus.DONE:
                friend.tasks_refer_a_friend = TaskStatus.CLAIMED
                user.points += ActionPoints.TASKS_REFER_A_FRIEND.value
        
        elif claim_request.task == FriendsTask.ACTIVE_TICKETS:
            if friend.tasks_active_tickets == TaskStatus.DONE:
                friend.tasks_active_tickets = TaskStatus.CLAIMED
                user.points += ActionPoints.TASKS_ACTIVE_TICKETS.value

        elif claim_request.task == FriendsTask.JOIN_CHANNEL:
            if friend.tasks_join_channel == TaskStatus.DONE:
                friend.tasks_join_channel = TaskStatus.CLAIMED
                user.points += ActionPoints.TASKS_JOIN_CHANNEL.value
            
                user.invited_users += 1

        else:
            raise HTTPException(status_code=400, detail="invalid_task")

        user_repository.session.add_all([user, friend])

    return ClaimResponse(friend_id=claim_request.friend_id, task=claim_request.task, new_points=user.points, new_tickets=user.invited_users + 1)