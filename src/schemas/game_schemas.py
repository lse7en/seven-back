from pydantic import BaseModel, model_validator
from datetime import datetime
from src.models.game import RpsGameStatus, RpsChoice
from typing_extensions import Self


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

    @model_validator(mode='after')
    def hide_choices_in_case_of_incomplete(self) -> Self:
        if self.status != RpsGameStatus.COMPLETED:
            self.player1_choice = None
            self.player2_choice = None
        return self

class RpsChoiceSchema(BaseModel):
    choice: RpsChoice

