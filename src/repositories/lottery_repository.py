from datetime import datetime, timedelta, UTC
from sqlalchemy import func, select, update
from sqlalchemy.orm import joinedload, load_only

from src.core.database import DBSession
from src.models.user import User
from src.models import lottery


class LotteryRepository:
    
        def __init__(self, session: DBSession):
            self.session = session
    
    
        async def update_and_get_index(self, lottery_id: int) -> int:
            """
            Update last_ticket_index and return it.

            :param lottery_id: id of lottery.
            :return: last_ticket_index.
            """
            query = update(lottery.Lottery).where(lottery.Lottery.id == lottery_id).values(
                last_ticket_index=lottery.Lottery.last_ticket_index + 1
            ).returning(lottery.Lottery.last_ticket_index)

            raw_index = await self.session.execute(query)
            return raw_index.scalar_one()
        
        async def get_lottery_ticket_for_index(self, lottery_id: int, ticket_index: int) -> int:
            """
            Get ticket in with ticket_index in lottery.tickets array.

            :param lottery_id: id of lottery.
            :param ticket_index: index of ticket.
            :return: ticket number.
            """
            query = select(lottery.Lottery.tickets[ticket_index]).where(lottery.Lottery.id == lottery_id)

            raw_ticket = await self.session.execute(query)
            return raw_ticket.scalar_one()
        

        async def add_lottery(self, lottery: lottery.Lottery):
            
            self.session.add(lottery)
            await self.session.flush()


        async def get_lottery_for_update(self, lottery_id: int) -> lottery.Lottery | None:

            query = select(lottery.Lottery).where(lottery.Lottery.id == lottery_id)\
            .options(load_only(lottery.Lottery.id, lottery.Lottery.pot, lottery.Lottery.last_ticket_index))

            raw_lottery = await self.session.execute(query.with_for_update())
            return raw_lottery.scalar_one_or_none()



class ParticipantRepository:

    def __init__(self, session: DBSession):
        self.session = session


    


    async def get_participant(self, user_id: int, lottery_id: int) -> lottery.Participant | None:
        """
        Get participant by user_id and lottery_id.

        :param user_id: id of user.
        :param lottery_id: id of lottery.
        :return: participant instance.
        """
        query = select(lottery.Participant).where(
            lottery.Participant.user_id == user_id,
            lottery.Participant.lottery_id == lottery_id
        ).options(joinedload(lottery.Participant.user, innerjoin=True)).options(joinedload(lottery.Participant.tickets))


        raw_participant = await self.session.execute(query)
        return raw_participant.unique().scalar_one_or_none()


    async def get_participant_for_update(self, user_id: int, lottery_id: int) -> lottery.Participant | None:
        """
        Get participant by user_id and lottery_id for update.

        :param user_id: id of user.
        :param lottery_id: id of lottery.
        :return: participant instance.
        """
        query = select(lottery.Participant).where(
            lottery.Participant.user_id == user_id,
            lottery.Participant.lottery_id == lottery_id
        ).options(joinedload(lottery.Participant.user, innerjoin=True))

        raw_participant = await self.session.execute(query.with_for_update())
        return raw_participant.scalar_one_or_none()



    async def add_participant(self, participant: lottery.Participant) -> None:
        """
        Add single participant to session and return it.

        :param participant: participant instance.
        :return: participant instance.
        """
        self.session.add(participant)
        await self.session.flush()

