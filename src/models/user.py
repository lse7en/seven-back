from sqlalchemy import (
    BigInteger,
    Integer,
    DateTime,
    DATE
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from src.core.model import Base
from datetime import datetime, date
from aiogram.utils.payload import  encode_payload

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    invited_users: Mapped[int] = mapped_column(Integer, default=0)
    joined: Mapped[bool] = mapped_column(default=False, nullable=False)
    referrer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    referrer = relationship("User", back_populates="invitees", remote_side=id)


    last_check_in: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    last_lucky_push: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    push_points: Mapped[int] = mapped_column(default=0)
    points: Mapped[int] = mapped_column(default=1000, index=True)

    language: Mapped[str] = mapped_column(default="en")
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)


    invitees = relationship("User", back_populates="referrer", remote_side=referrer_id)

    referrer_score: Mapped[bool] = mapped_column(default=False, nullable=False)

    static_rank: Mapped[int] = mapped_column(default=1000, nullable=False, index=True)

    last_secret_code_date: Mapped[date] = mapped_column(DATE, nullable=False, default=date(2021, 1, 1))


    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}" if self.last_name else self.first_name


    @property
    def info(self) -> str:
        return f"id({self.id}): {self.full_name} @{self.username}; jnd: {self.joined}; inv: {self.invited_users} pnts: {self.points} ref: {self.referrer_id}"
    

    @property
    def full_info(self) -> str:
        return f"{self.info}" + (f"\nreferrer: \n{self.referrer.info}" if self.referrer else "")
    
    @property
    def ref_link(self) -> str:
        return f"https://t.me/the_lucky_7_bot/main?startapp={encode_payload(str(self.id))}"
