from typing import Optional

from sqlalchemy import func, select

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
    

    async def get_user_rank(self, user_id: int):
        """
        Get user rank using func.rank

        :param user_id: id of user.
        :return: rank of user.
        """

        raw = await self.session.execute(
            select(func.rank().over(order_by=User.invited_users)).where(User.id == user_id),
        )
        return raw.scalars().all()