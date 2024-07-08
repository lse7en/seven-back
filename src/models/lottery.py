from sqlalchemy import (
    BigInteger,
    Integer,
    DateTime,
    DATE
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY
from src.core.model import Base
from src.models.user import User
from datetime import datetime



class Lottery(Base):
    __tablename__ = "lotteries"
    pot: Mapped[int] = mapped_column(Integer, default=0)
    tickets: Mapped[list[int]] = mapped_column(ARRAY(Integer), default=[])
    last_ticket_index: Mapped[int] = mapped_column(Integer, default=0)

    jackpot: Mapped[int] = mapped_column(Integer, nullable=True, default=None)
    draw_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True, default=None)
    finish_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True, default=None)


class Participant(Base):
    __tablename__ = "participants"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped[User] = relationship(User)

    lottery_id: Mapped[int] = mapped_column(ForeignKey("lotteries.id"), nullable=False)

    activate_tickets_count: Mapped[int] = mapped_column(Integer, default=0)

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="participant")

    __table_args__ = (UniqueConstraint('lottery_id', 'user_id', name='participants_lottery_user_unx'),)




class Ticket(Base):
    __tablename__ = "tickets"

    lottery_id: Mapped[int] = mapped_column(ForeignKey("lotteries.id"), nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped[User] = relationship(User)

    participant_id: Mapped[int] = mapped_column(ForeignKey("participants.id"), nullable=False)
    participant: Mapped[Participant] = relationship(Participant, back_populates="tickets")

    ticket_index: Mapped[int] = mapped_column(Integer, nullable=False)
    ticket_number: Mapped[int] = mapped_column(Integer, nullable=False)

    matched: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    __table_args__ = (UniqueConstraint('lottery_id', 'ticket_index', name='tickets_lottery_index_unx'), (UniqueConstraint('lottery_id', 'ticket_number', name='tickets_lottery_number_unx')))
