# from sqlalchemy import (
#     BigInteger,
#     Integer,
#     DateTime,
#     DATE
# )
# from sqlalchemy.orm import Mapped, mapped_column
# from sqlalchemy import ForeignKey, UniqueConstraint
# from sqlalchemy.dialects.postgresql import ARRAY
# from src.core.model import Base
# from datetime import datetime



# class Lottery(Base):
#     __tablename__ = "lotteries"
#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     pot: Mapped[int] = mapped_column(Integer, default=0)
#     tickets: Mapped[list[int]] = mapped_column(ARRAY(Integer), default=[])
#     last_ticket_index: Mapped[int] = mapped_column(Integer, default=1)

#     jackpot: Mapped[int] = mapped_column(Integer, nullable=True, default=None)
#     draw_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True, default=None)
#     finish_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

# class Ticket(Base):
#     __tablename__ = "tickets"
#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
#     lottery_id: Mapped[int] = mapped_column(ForeignKey("lotteries.id"), nullable=False)
#     ticket_index: Mapped[int] = mapped_column(Integer, nullable=False)
#     ticket_number: Mapped[int] = mapped_column(Integer, nullable=False)

#     __table_args__ = (UniqueConstraint('lottery_id', 'ticket_index', name='ticket_lottery_unx'),)
