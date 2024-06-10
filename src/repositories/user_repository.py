from typing import Optional

from datetime import datetime
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

from src.core.database import DBSession
from src.models.user import User


class UserRepository:
    """
    Class for accessing user table.

    This class provides methods to interact with the user table in the database.
    """

    def __init__(self, session: DBSession):
        self.session = session

    async def count(self) -> int:
        """
        Get count of users.

        :return: count of users.
        """
        raw = await self.session.execute(func.count(User.id))
        return raw.scalar()

    async def add_user(self, user: User) -> None:
        """
        Add single user to session and return it.

        :param user: user instance.
        :return: user instance.
        """
        self.session.add(user)
        await self.session.flush()


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
