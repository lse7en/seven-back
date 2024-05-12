from sqlalchemy import (
    BigInteger,
    Integer,
    DateTime
)
from sqlalchemy.orm import Mapped, mapped_column

from src.core.model import Base
from datetime import datetime
from math import log2


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    invited_by_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    invited_users: Mapped[int] = mapped_column(Integer, default=0)
    last_check_in: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    language: Mapped[str] = mapped_column(default="en")


    @property
    def points(self) -> float:
        return 1 + log2(1 + self.invited_users)