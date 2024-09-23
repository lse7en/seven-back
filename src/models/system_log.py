import enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum
from src.core.model import Base

from src.models.user import User


class LogTag(enum.Enum):
    PUSH = "push"
    SECRET = "secret"
    SCRATCH = "scratch"
    ADS_DOUBLE = "ads_double"
    ADS_POINT = "ads_point"




class SystemLog(Base):
    __tablename__ = "system_logs"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped[User] = relationship(User)
    command: Mapped[str] = mapped_column(nullable=False)
    tag: Mapped[LogTag] = mapped_column(Enum(LogTag), nullable=True)
