from sqlalchemy import (
    DateTime,
    ForeignKey,
    Enum as SQLEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from src.core.model import Base
from src.models.user import User
from enum import Enum as PyEnum


class RpsGameStatus(PyEnum):
    WAITING_FOR_PLAYER = "waiting_for_player"
    WAITING_FOR_CHOICES = "waiting_for_choices"
    COMPLETED = "completed"


class RpsChoice(PyEnum):
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"


class RpsGame(Base):
    __tablename__ = "rps_games"

    player1_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    # player1: Mapped[User] = relationship(User, foreign_keys=[player1_id])
    player2_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    # player2: Mapped[User | None] = relationship(User, foreign_keys=[player2_id])

    player1_choice: Mapped[RpsChoice] = mapped_column(SQLEnum(RpsChoice), nullable=True)
    player2_choice: Mapped[RpsChoice] = mapped_column(SQLEnum(RpsChoice), nullable=True)

    status: Mapped[RpsGameStatus] = mapped_column(
        SQLEnum(RpsGameStatus), default=RpsGameStatus.WAITING_FOR_PLAYER, nullable=False
    )

    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )



    @property
    def winner(self):

    # Returns 1 if player1 wins, 2 if player2 wins, 0 if tie

        if self.player1_choice and not self.player2_choice:
            return self.player1_id
        elif not self.player1_choice and self.player2_choice:
            return self.player2_id
        elif not self.player1_choice and not self.player2_choice:
            return 0
        else:
            rules = {
                RpsChoice.ROCK: RpsChoice.SCISSORS,
                RpsChoice.PAPER: RpsChoice.ROCK,
                RpsChoice.SCISSORS: RpsChoice.PAPER,
            }
            if self.player1_choice == self.player2_choice:
                return 0
            elif rules[self.player1_choice] == self.player2_choice:
                return self.player1_id
            else:
                return self.player2_id