

from typing import Optional
from src.core.schema import BaseModel




class UserBase(BaseModel):
    """
    DTO for User model.

    It returned when accessing User models from the API.
    """

    id: int
    full_name: str
    photo_url: Optional[str] = None
    joined: bool
    created_at: str





class User(UserBase):
    """DTO for User model."""

    invited_users: int
    points: float
    ref_link: str
    friends: list[UserBase] = []
