from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum
from src.core.model import Base
from src.models.enums import LogTag
from src.models.user import User




class SystemLog(Base):
    __tablename__ = "system_logs"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped[User] = relationship(User)
    command: Mapped[str] = mapped_column(nullable=False)
    tag: Mapped[LogTag] = mapped_column(Enum(LogTag), nullable=True)
