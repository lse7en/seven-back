
from typing import Annotated
from fastapi import APIRouter, Depends

from src.deps import  CurrentUser
from src.core.database import DBSession
from src.schemas.user_schemas import User
import random
from src.repositories.user_repository import UserRepository
from src.repositories.system_log_repository import SystemLogRepository
from src.models.system_log import SystemLog
router = APIRouter(prefix="/rank", tags=["rank"])


@router.get("", response_model=User)
async def rank(
    current_user: CurrentUser,
    user_repository: Annotated[UserRepository, Depends()],
    system_log_repository: Annotated[SystemLogRepository, Depends()]
):
    rank = await user_repository.get_user_rank(current_user.id)
    # rank = current_user.static_rank
    current_user.rank = rank
    # await system_log_repository.add_log(SystemLog(user=current_user, command=f"rank:{rank}"))
    current_user.min_invitations = 0
    current_user.min_points = 0
    return current_user

    # if rank > 20:
    #     min_invitations = await user_repository.get_min_invitation_count_for_rank(20)
    #     min_points = await user_repository.get_min_points_for_rank(20)

    #     current_user.min_invitations = min_invitations
    #     current_user.min_points = min_points

    # return current_user