from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from src.models.game import RpsGame, RpsGameStatus
from src.models.user import User
import random
from src.core.database import DBSession


class RpsGameRepository:
    def __init__(self, session: DBSession):
        self.session = session

    async def get_waiting_game(self):
        result = await self.session.execute(
            select(RpsGame).where(RpsGame.status == RpsGameStatus.WAITING_FOR_PLAYER).with_for_update()
        )
        return result.scalars().first()

    async def add_game(self, game: RpsGame):
        self.session.add(game)
        await self.session.flush()

    async def update_game(self, game: RpsGame):
        await self.session.flush()

    async def get_active_game_for_user(self, user_id: int):
        result = await self.session.execute(
            select(RpsGame).where(
                and_(
                    RpsGame.status != RpsGameStatus.COMPLETED,
                    or_(RpsGame.player1_id == user_id, RpsGame.player2_id == user_id),
                )
            )
        )
        return result.scalars().first()
