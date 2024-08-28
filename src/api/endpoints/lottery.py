
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from src.deps import  CurrentUserId
from src.core.database import DBSession
from src.schemas.lottery_schema import Participant as ParticipantSchema, LotteryList, Lottery as LotterySchema

from src.models.lottery import Participant, Ticket
from src.repositories.user_repository import UserRepository
from src.repositories.lottery_repository import ParticipantRepository, LotteryRepository
from src.repositories.system_log_repository import SystemLogRepository
from src.models.system_log import SystemLog

router = APIRouter(prefix="/lotteries", tags=["lottery"])

ACTIVE_LOTTERY_ID = 6






@router.get("", response_model=LotteryList)
async def get_lotteries(
    session: DBSession,
    lottery_repository: Annotated[LotteryRepository, Depends()],
):
    async with session.begin():
        lotteries = await lottery_repository.get_lotteries_with_id_less_than(ACTIVE_LOTTERY_ID)
        

    return LotteryList(
        items=[LotterySchema.model_validate(lot, from_attributes=True) for lot in lotteries]
    )

@router.get("/active/participant", response_model=ParticipantSchema)
async def get_active_participant(
    user_id: CurrentUserId,
    session: DBSession,
    participant_repository: Annotated[ParticipantRepository, Depends()]
):

    return await get_participant(ACTIVE_LOTTERY_ID, user_id, session, participant_repository)

@router.get("/{lottery_id}/participant", response_model=ParticipantSchema)
async def get_participant(
    lottery_id: int,
    user_id: CurrentUserId,
    session: DBSession,
    participant_repository: Annotated[ParticipantRepository, Depends()],
):
    async with session.begin():
        participant = await participant_repository.get_participant(user_id, lottery_id)

        if participant:
            return participant
        
        try:
            await participant_repository.add_participant(Participant(user_id=user_id, lottery_id=lottery_id))
        except Exception as e:
            print("should_not_happen", e)
        
    
    async with session.begin():
        return await participant_repository.get_participant(user_id, lottery_id)
        






@router.post("/activate", response_model=ParticipantSchema)
async def activate(
    user_id: CurrentUserId,
    session: DBSession,
    lottery_repository: Annotated[LotteryRepository, Depends()],
    participant_repository: Annotated[ParticipantRepository, Depends()],
    system_log_repository: Annotated[SystemLogRepository, Depends()]
):
    
    lottery_id = ACTIVE_LOTTERY_ID

    async with session.begin():
        participant = await participant_repository.get_participant_for_update(user_id, lottery_id)

        if not participant:
            raise HTTPException(status_code=404, detail="Participant not found")

        if participant.inactivate_tickets_count <= 0:
            return await participant_repository.get_participant(user_id, lottery_id)
        
        if participant.user.points < 2000:
            return await participant_repository.get_participant(user_id, lottery_id)
        

        participant.activate_tickets_count += 1
        participant.user.points -= 2000
        participant.lottery.last_ticket_index += 1
        ticket_index = participant.lottery.last_ticket_index
        ticket_number = await lottery_repository.get_lottery_ticket_for_index(lottery_id, ticket_index)

        ticket = Ticket(lottery_id=lottery_id, user=participant.user, participant_id=participant.id, ticket_index=ticket_index, ticket_number=ticket_number)

        session.add(ticket)
        await session.flush()
        await system_log_repository.add_log(SystemLog(user=participant.user, command=f"🟢 ticket 🟢: {ticket_index}"))
        await participant_repository.add_participant(participant)


    return await participant_repository.get_participant(user_id, lottery_id)
