from fastapi import APIRouter, Depends, Request
from src.core.schema import BaseModel
from src.models.enums import FriendsTask
from src.deps import CurrentUserId
from src.core.database import DBSession



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
    session: DBSession,
):
    pass
