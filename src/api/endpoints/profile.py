
from fastapi import APIRouter

from src.deps import  CurrentUser
from src.schemas.user_schemas import User

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", response_model=User)
async def profile(
    current_user: CurrentUser,
):
    return current_user