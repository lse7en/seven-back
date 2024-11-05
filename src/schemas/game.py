from pydantic import BaseModel
from datetime import datetime
from src.models.game import GameStatus, Choice


class RpsGameSchema(BaseModel):
    id: int
    player1_id: int
    player2_id: int | None
    player1_choice: Choice | None
    player2_choice: Choice | None
    status: GameStatus
    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None

    class Config:
        orm_mode = True


class RpsChoiceSchema(BaseModel):
    choice: Choice


class RpsGameResultSchema(BaseModel):
    result: int | None  # 1 if player1 wins, 2 if player2 wins, 0 if tie
    game: GameSchema
