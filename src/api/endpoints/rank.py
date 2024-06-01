
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
    await system_log_repository.add_log(SystemLog(user=current_user, command="get:rank"))
    rank = await user_repository.get_user_rank(current_user.id)
    current_user.rank = rank

    if rank > 20:
        min_invitations = await user_repository.get_min_invitation_count_for_rank(20)

        current_user.min_invitations = min_invitations

    return current_user