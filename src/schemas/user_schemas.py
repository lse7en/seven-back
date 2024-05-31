

from typing import Optional
from src.core.schema import BaseModel
from datetime import datetime



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





class User(UserBase):
    """DTO for User model."""

    invited_users: int
    points: float
    ref_link: str
    friends: list[UserBase] = []
    last_lucky_push: datetime
    rank: Optional[int] = None
    min_invitations: Optional[int] = None


class Rank(BaseModel):
    """DTO for User rank."""

    rank: int