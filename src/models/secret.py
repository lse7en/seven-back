from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UniqueConstraint

from src.core.model import Base
from datetime import date


class SecretCode(Base):
    __tablename__ = "secret_codes"
    key: Mapped[date] = mapped_column(Date(), index=True, nullable=False)
    secret: Mapped[str] = mapped_column(nullable=False)

    __table_args__ = (UniqueConstraint('key', 'secret', name='secret_codes_key_secret_unx'),)
