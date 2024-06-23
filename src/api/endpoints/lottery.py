
from typing import Annotated
from fastapi import APIRouter, Depends

from src.deps import  CurrentUser
from src.core.database import DBSession
from src.schemas.user_schemas import User

from src.models.lottery import Participant
from src.repositories.user_repository import UserRepository
from src.repositories.lottery_repository import ParticipantRepository
from src.repositories.system_log_repository import SystemLogRepository
from src.models.system_log import SystemLog

router = APIRouter(prefix="/lottery", tags=["lottery"])


lottery_id = 1


@router.get("/participant", response_model=User)
async def participant(
    current_user: CurrentUser,
    session: DBSession,
    user_repository: Annotated[UserRepository, Depends()],
    participant_repository: Annotated[ParticipantRepository, Depends()],
    system_log_repository: Annotated[SystemLogRepository, Depends()]
):
    u_id = current_user.id

    async with session.begin():
        participant = await participant_repository.get_participant(u_id, lottery_id)

        if participant:
            return participant
        
        try:
            participant = await participant_repository.add_participant(Participant(user_id=u_id, lottery_id=lottery_id))
            return participant
        except Exception as e:
            print("should_not_happen", e)
            return await participant_repository.get_participant(u_id, lottery_id)