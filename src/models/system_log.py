
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from src.core.model import Base

from src.models.user import User

class SystemLog(Base):
    __tablename__ = "system_logs"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped[User] = relationship(User)
    command: Mapped[str] = mapped_column(nullable=False)
