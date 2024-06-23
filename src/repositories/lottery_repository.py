from datetime import datetime, timedelta, UTC
from sqlalchemy import func, select, update
from sqlalchemy.orm import joinedload

from src.core.database import DBSession
from src.models.user import User
from src.models import lottery

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
        raw_participant = await self.session.execute(
            select(lottery.Participant).where(
                lottery.Participant.user_id == user_id,
                lottery.Participant.lottery_id == lottery_id
            ).options(joinedload(lottery.Participant.user)).options(joinedload(lottery.Participant.tickets))
        )
        return raw_participant.scalar_one_or_none()
    


    async def add_participant(self, participant: lottery.Participant) -> None:
        """
        Add single participant to session and return it.

        :param participant: participant instance.
        :return: participant instance.
        """
        self.session.add(participant)
        await self.session.flush()

    async def get_user_for_update(self, user_id: int) -> User:
        """
        Get user for update.

        :param user_id: id of user.
        :return: user instance.
        """
        raw_user = await self.session.execute(
            select(User).where(User.id == user_id).with_for_update()
        )
        return raw_user.scalar_one_or_none()


    async def get_user_or_none_by_id(self, user_id: int) -> Optional[User]:
        """
        Get user by id.

        :param user_id: id of user.
        :return: user instance.
        """
        raw_user = await self.session.execute(
            select(User).where(User.id == user_id),
        )
        return raw_user.scalars().first()


    async def get_all_users(self):
        """
        Get all users.

        :return: list of user instances.
        """
        raw_users = await self.session.execute(select(User))
        return raw_users.scalars().all()
    
    async def get_not_joined_users(self) -> list[User]:
        """
        Get all users who have not joined the community.

        :return: list of user instances.
        """
        raw_users = await self.session.execute(select(User).where(User.joined == False))  # noqa: E712
        return raw_users.scalars().all()
    

    async def get_joined_users(self) -> list[User]:
        """
        Get all users who have joined the community.

        :return: list of user instances.
        """
        raw_users = await self.session.execute(select(User).where(User.joined == True))  # noqa: E712
        return raw_users.scalars().all()
    

    async def get_user_rank(self, user_id: int) -> int:
        """
        Get user rank using func.rank

        :param user_id: id of user.
        :return: rank of user.
        """
        subq = select(User.id, func.rank().over(order_by=User.points.desc()).label('rank')).subquery()

        raw = await self.session.execute(
            select(subq.c.rank).where(subq.c.id == user_id)
        )
        return raw.scalar_one()
    

    async def get_min_invitation_count_for_rank(self, max_rank: int) -> int:
        """
        Get minimum invitation count for a rank.
        
        :param max_rank: maximum rank.
        :return: minimum invitation count.
        """
        subq = select(User.invited_users, func.rank().over(order_by=User.points.desc()).label('rank')).subquery()

        # select first row with rank less than or equal to max_rank
        raw = await self.session.execute(
            select(subq.c.invited_users).where(subq.c.rank <= max_rank).order_by(subq.c.rank.desc()).limit(1)
        )
        return raw.scalar_one()
    

    async def get_min_points_for_rank(self, max_rank: int) -> float:
        """
        Get minimum points for a rank.
        
        :param max_rank: maximum rank.
        :return: minimum points.
        """
        subq = select(User.points, func.rank().over(order_by=User.points.desc()).label('rank')).subquery()

        # select first row with rank less than or equal to max_rank
        raw = await self.session.execute(
            select(subq.c.points).where(subq.c.rank <= max_rank).order_by(subq.c.rank.desc()).limit(1)
        )
        return raw.scalar_one()
    


    async def get_users_with_ranking(self, limit: int):

        subq = select(User, func.rank().over(order_by=User.points.desc()).label('rank')).subquery()

        raw_users = await self.session.execute(
            select(subq.c.id).select_from(subq).order_by(subq.c.rank).limit(limit)
        )
        return raw_users.scalars().all()
    

    async def get_top_users(self, limit: int) -> list[User]:
        """
        Get top users.

        :param limit: limit of users.
        :return: list of user instances.
        """
        raw_users = await self.session.execute(
            select(User).order_by(User.static_rank.asc()).limit(limit)
        )
        return raw_users.scalars().all()
    

    async def get_users_with_ids_in(self, ids: list[int]) -> list[User]:
        """
        Get users with ids in list.

        :param ids: list of user ids.
        :return: list of user instances.
        """
        raw_users = await self.session.execute(
            select(User).where(User.id.in_(ids))
        )
        return raw_users.scalars().all()
    

    async def count_active_users_since_last_hour(self, hour: int) -> int:
        """
        Count active users since last hour.

        :param hour: hour.
        :return: count of active users.
        """
        raw = await self.session.execute(
            select(func.count(User.id)).where(User.last_check_in > datetime.now(UTC) - timedelta(hours=hour))
        )
        return raw.scalar()


    async def get_users_order_by_join_and_limit(self, last_date: datetime, limit: int) -> list[User]:
        """
        Get all users who joined after last_date.

        :param last_date: last date.
        :param limit: limit of users.
        :return: list of user instances.
        """
        raw_users = await self.session.execute(
            select(User).options(joinedload(User.referrer))
            .where(User.created_at > last_date).order_by(User.created_at).limit(limit)
        )
        return raw_users.scalars().all()
    
    async def get_friends(self, user_id) -> list[User]:
        """
        Get all friends of user.

        :param user: user instance.
        :return: list of user instances.
        """
        raw_friends = await self.session.execute(
            select(User).where(User.referrer_id == user_id).order_by(User.created_at.desc())
        )
        return raw_friends.scalars().all()


    async def set_static_rank_for_all(self):

        subq = select(User.id, func.rank().over(order_by=User.points.desc()).label('rank'))


        update_stmt = update(User).values(static_rank=subq.c.rank).where(User.id == subq.c.id)

        await self.session.execute(update_stmt)