

from typing import Optional

from pydantic import computed_field
from src.core.schema import BaseModel
from datetime import datetime, date
from src.models.enums import TaskStatus


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
    tasks_join_channel: TaskStatus
    tasks_active_tickets: TaskStatus
    tasks_refer_a_friend: TaskStatus
    tasks_secret_code: TaskStatus
    tasks_watch_ads: TaskStatus

    invited_users: int


class UserFriend(UserBase):
    """DTO for User model."""

    active_tickets_count: int




    @computed_field
    @property
    def number_of_done_tasks(self) -> int:
        return sum([
            self.tasks_join_channel == TaskStatus.CLAIMED,
            self.tasks_active_tickets == TaskStatus.CLAIMED,
            self.tasks_refer_a_friend == TaskStatus.CLAIMED,
            self.tasks_secret_code == TaskStatus.CLAIMED,
            self.tasks_watch_ads == TaskStatus.CLAIMED,
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
    next_ad_for_points: datetime
    next_push_time: datetime
    secret_reset_datetime: datetime
    join_reward: bool
    current_rps_game_id: Optional[int] = None



class Rank(BaseModel):
    """DTO for User rank."""

    rank: int



class Language(BaseModel):
    """DTO for User language info."""
    lang: str