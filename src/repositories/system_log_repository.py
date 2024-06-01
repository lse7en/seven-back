from typing import Optional

from datetime import datetime
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

from src.core.database import DBSession
from src.models.system_log import SystemLog

class SystemLogRepository:

    def __init__(self, session: DBSession):
        self.session = session

    async def get_logs_order_by_time_and_limit(self, last_date: datetime, limit: int) -> list[SystemLog]:
        """
        Get all users who joined after last_date.

        :param last_date: last date.
        :param limit: limit of users.
        :return: list of user instances.
        """
        raw_users = await self.session.execute(
            select(SystemLog).options(joinedload(SystemLog.user))
            .where(SystemLog.created_at > last_date).order_by(SystemLog.created_at).limit(limit)
        )
        return raw_users.scalars().all()
    

    async def add_log(self, log: SystemLog) -> None:
        """
        Add single user to session and return it.

        :param user: user instance.
        :return: user instance.
        """
        self.session.add(log)
        await self.session.flush()