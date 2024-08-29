
from datetime import date
from sqlalchemy import select

from src.core.database import DBSession
from src.models.secret import SecretCode

class SecretCodeRepository:

    def __init__(self, session: DBSession):
        self.session = session



    async def add(self, sc: SecretCode) -> None:
        self.session.add(sc)
        await self.session.flush()


    async def exists(self, key: date, secret: str) -> bool:
        raw = await self.session.execute(
            select(SecretCode).where(SecretCode.key == key, SecretCode.secret == secret)
        )
        return raw.scalar_one_or_none() is not None
    

    async def get_by_key(self, key: date) -> SecretCode | None:
        raw = await self.session.execute(
            select(SecretCode).where(SecretCode.key == key)
        )
        return raw.scalar_one_or_none()