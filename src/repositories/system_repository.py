from typing import Optional

from datetime import datetime
from sqlalchemy import func, select

from src.core.database import DBSession
from src.models.system import System


class SystemRepository:

    def __init__(self, session: DBSession):
        self.session = session


    async def update(self, system: System) -> None:

        self.session.add(system)
        await self.session.flush()


    async def get(self) -> System:

        raw_user = await self.session.execute(
            select(System).limit(1).with_for_update()
        )
        return raw_user.scalar_one()


