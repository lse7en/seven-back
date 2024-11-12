from sqlalchemy import (
    BigInteger,
    Integer,
    DateTime,
    DATE,
    Boolean,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum
from src.core.model import Base
from datetime import datetime, date, timedelta, time, UTC
from aiogram.utils.payload import  encode_payload
from src.models.enums import TaskStatus

def one_month_age():
    return datetime.utcnow() - timedelta(days=365)





class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    is_bot: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    invited_users: Mapped[int] = mapped_column(Integer, default=0)
    joined: Mapped[bool] = mapped_column(default=False, nullable=False)
    referrer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    referrer = relationship("User", back_populates="invitees", remote_side=id)

    join_reward: Mapped[bool] = mapped_column(default=False, nullable=False)

    last_check_in: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    last_lucky_push: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    push_points: Mapped[int] = mapped_column(default=0)
    points: Mapped[int] = mapped_column(default=0, index=True)
    push_count: Mapped[int] = mapped_column(default=0)

    language: Mapped[str] = mapped_column(default="en")
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)

    custom_lang: Mapped[str] = mapped_column(nullable=False, default="en")


    invitees = relationship("User", back_populates="referrer", remote_side=referrer_id)


    static_rank: Mapped[int] = mapped_column(default=1000, nullable=False, index=True)

    last_secret_code_date: Mapped[date] = mapped_column(DATE, nullable=False, default=date(2021, 1, 1))


    total_ads_watched: Mapped[int] = mapped_column(default=0)
    total_ads_watched_this_push: Mapped[int] = mapped_column(default=0)

    last_ads_watch_for_points: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=one_month_age)
    total_ads_watched_for_points: Mapped[int] = mapped_column(default=0)


    src: Mapped[str] = mapped_column(nullable=True, index=True, default=None)

    tasks_join_channel: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.NOT_DONE, nullable=False)
    tasks_active_tickets: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.NOT_DONE, nullable=False)
    tasks_refer_a_friend: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.NOT_DONE, nullable=False)
    tasks_secret_code: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.NOT_DONE, nullable=False)
    tasks_watch_ads: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.NOT_DONE, nullable=False)

    current_rps_game_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, default=None)



    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}" if self.last_name else self.first_name
    

    @property
    def age(self) -> int:
        # age in days from created_at
        return (datetime.now(UTC) - self.created_at).days


    @property
    def info(self) -> str:
        return f"id({self.id}): {self.full_name} @{self.username}; jnd: {self.joined}; inv: {self.invited_users} pnts: {self.points} age: {self.age} ref: {self.referrer_id}"
    

    @property
    def full_info(self) -> str:
        return f"{self.info}" + (f"\nreferrer: \n{self.referrer.info}" if self.referrer else "")
    
    @property
    def ref_link(self) -> str:
        return f"https://t.me/the_lucky_7_bot/main?startapp={encode_payload(str(self.id))}"

    @property
    def push_waiting_time(self) -> int:
        return (2 ** (3 - min(4, self.invited_users))) * 60

    @property
    def ads_reduce_time(self) -> int:

        if self.total_ads_watched_this_push > 5:
            return 0

        return int(self.push_waiting_time // (self.total_ads_watched_this_push * 2 + 10))
    

    @property
    def next_push_time(self) -> datetime:
        return self.last_lucky_push + timedelta(minutes=self.push_waiting_time)
    

    @property
    def next_ad_for_points(self) -> datetime:
        return self.last_ads_watch_for_points + timedelta(minutes=10)
    

    @property
    def secret_reset_datetime(self) -> datetime:
        # create a date time in utc timezone with the given date and time 16:00:00
        return datetime.combine(self.last_secret_code_date, time(16, 0, 0), tzinfo=UTC) + timedelta(days=1)