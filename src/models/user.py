from sqlalchemy import (
    BigInteger,
    Integer,
    DateTime
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from src.core.model import Base
from datetime import datetime
from math import log2


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    invited_users: Mapped[int] = mapped_column(Integer, default=0)
    last_check_in: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    language: Mapped[str] = mapped_column(default="en")
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)
    joined: Mapped[bool] = mapped_column(default=False, nullable=False)
    referrer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    referrer = relationship("User", back_populates="invitees")



    @property
    def points(self) -> float:
        return 1 + log2(1 + self.invited_users)
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


    @property
    def info(self) -> str:
        return f"id({self.id}): {self.full_name} @{self.username}; joined: {self.joined}; invited_users: {self.invited_users} language: {self.language}, referrer: {self.referrer_id}"