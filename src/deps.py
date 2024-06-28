from typing import Annotated

import jwt
from fastapi import Depends, Header, HTTPException, status
from jwt.exceptions import InvalidTokenError

from src.settings import Settings, get_settings

SettingsDep = Annotated[Settings, Depends(get_settings)]


async def get_current_user_id(
    settings: SettingsDep,
    tg_data: Annotated[str | None, Header()] = None,
) -> int:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            tg_data, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return user_id
    except InvalidTokenError:
        raise credentials_exception


CurrentUserId = Annotated[int, Depends(get_current_user_id)]
