from sqlalchemy import (
    BigInteger,
    Integer,
    DateTime,
    String,
    ForeignKey,
    Enum as SQLEnum,
    Boolean,
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

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    player1_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    player1: Mapped[User] = relationship(User, foreign_keys=[player1_id])
    player2_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    player2: Mapped[User] = relationship(User, foreign_keys=[player2_id])

    player1_choice: Mapped[RpsChoice] = mapped_column(SQLEnum(RpsChoice), nullable=True)
    player2_choice: Mapped[RpsChoice] = mapped_column(SQLEnum(RpsChoice), nullable=True)

    status: Mapped[RpsGameStatus] = mapped_column(
        SQLEnum(RpsGameStatus), default=RpsGameStatus.WAITING_FOR_PLAYER, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
