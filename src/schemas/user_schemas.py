

from typing import Optional

from pydantic import computed_field
from src.core.schema import BaseModel
from datetime import datetime, date



class UserBase(BaseModel):
    """
    DTO for User model.

    It returned when accessing User models from the API.
    """

    id: int
    full_name: str
    photo_url: Optional[str] = None
    joined: bool
    created_at: datetime
    username: Optional[str] = None


    #tasks info
    tasks_join_channel: str
    tasks_active_tickets: str
    tasks_refer_a_friend: str
    tasks_secret_code: str
    tasks_watch_ads: str

    invited_users: int


class UserFriend(UserBase):
    """DTO for User model."""

    active_tickets_count: int




    @computed_field
    @property
    def number_of_done_tasks(self) -> int:
        return sum([
            self.tasks_join_channel == "done",
            self.tasks_active_tickets == "done",
            self.tasks_refer_a_friend == "done",
            self.tasks_secret_code == "done",
            self.tasks_watch_ads == "done",
        ])


class User(UserBase):
    """DTO for User model."""

    invited_users: int
    points: float
    ref_link: str
    friends: list[UserBase] = []
    last_lucky_push: datetime
    rank: Optional[int] = None
    min_invitations: Optional[int] = None
    min_points: Optional[float] = None
    last_secret_code_date: date
    ads_reduce_time: int
    push_waiting_time: int
    next_ad_for_points: datetime
    next_push_time: datetime
    secret_reset_datetime: datetime
    join_reward: bool


class Rank(BaseModel):
    """DTO for User rank."""

    rank: int