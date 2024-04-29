

from typing import Optional
from src.core.schema import BaseModel




class UserBase(BaseModel):
    """
    DTO for User model.

    It returned when accessing User models from the API.
    """

    id: int
    first_name: str
    telegram_id: int
    photo_url: Optional[str]

class User(BaseModel):
    """DTO for User model."""

    telegram_id: int
    last_name: str
    is_bot: bool
    username: Optional[str]
    language_code: str
    added_to_attachment_menu: bool
    allows_write_to_pm: bool
    is_premium: bool
    auth_date: int
