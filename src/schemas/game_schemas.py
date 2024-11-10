from pydantic import BaseModel
from datetime import datetime
from src.models.game import RpsGameStatus, RpsChoice


class PlayerSchema(BaseModel):
    id: int
    first_name: str
    last_name: str | None
    full_name: str


class RpsGameSchema(BaseModel):
    id: int
    player1: PlayerSchema
    player2: PlayerSchema | None
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

