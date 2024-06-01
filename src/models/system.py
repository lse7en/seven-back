from sqlalchemy import (
    Integer,
    DateTime
)
from sqlalchemy.orm import Mapped, mapped_column

from src.core.model import Base
from datetime import datetime


class System(Base):
    __tablename__ = "system"
    last_user_log: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.min,
    )
    max_user_cumulative = mapped_column(Integer, default=0)

    last_action_log: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.min,
    )
