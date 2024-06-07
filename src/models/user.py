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
from aiogram.utils.deep_linking import create_deep_link

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    invited_users: Mapped[int] = mapped_column(Integer, default=0)
    last_check_in: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    last_lucky_push: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    push_points: Mapped[int] = mapped_column(default=0)
    points: Mapped[int] = mapped_column(default=0, index=True)

    language: Mapped[str] = mapped_column(default="en")
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)
    joined: Mapped[bool] = mapped_column(default=False, nullable=False)

    referrer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    referrer = relationship("User", back_populates="invitees", remote_side=id)
    invitees = relationship("User", back_populates="referrer", remote_side=referrer_id)
    
    referrer_score: Mapped[bool] = mapped_column(default=False, nullable=False)

    
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}" if self.last_name else self.first_name


    @property
    def info(self) -> str:
        return f"id({self.id}): {self.full_name} @{self.username}; joined: {self.joined}; invited_users: {self.invited_users} language: {self.language} referrer: {self.referrer_id}"
    

    @property
    def full_info(self) -> str:
        return f"{self.info}" + (f"\nreferrer: \n{self.referrer.info}" if self.referrer else "")
    
    @property
    def ref_link(self) -> str:
        return create_deep_link(
        username="the_lucky_7_bot",
        link_type="start",
        payload=str(self.id),
        encode=True,
    )