from sqlalchemy import (
    BigInteger,
    Integer,
    DateTime
)
from sqlalchemy.orm import Mapped, mapped_column

from src.core.model import Base
from datetime import datetime
from math import log2


class System(Base):
    __tablename__ = "system"
    last_user_log = mapped_column(DateTime, default=datetime.min)
    max_user_cumulative = mapped_column(Integer, default=0)
