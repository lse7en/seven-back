from pydantic import BaseModel
from datetime import datetime
from src.models.game import RpsGameStatus, RpsChoice


class RpsGameSchema(BaseModel):
    id: int
    player1_id: int
    player2_id: int | None
    player1_choice: RpsChoice | None
    player2_choice: RpsChoice | None
    status: RpsGameStatus
    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None
    winner: int | None

    class Config:
        orm_mode = True


class RpsChoiceSchema(BaseModel):
    choice: RpsChoice

