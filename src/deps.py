import json
from typing import Annotated

from fastapi import Depends, Header, Request

from src.bot.constants import COMMUNITY_TID
from src.bot.validators import is_member_of
from src.core.database import DBSession
from src.core.exceptions import AuthRequired, InvalidToken
from src.core.security import validate_tg_data
from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.settings import Settings, get_settings
from datetime import datetime
SettingsDep = Annotated[Settings, Depends(get_settings)]



async def get_current_user(
    settings: SettingsDep,
    session: DBSession,
    request: Request,
    user_repository: Annotated[UserRepository, Depends()],
    tg_data: Annotated[str | None, Header()] = None,
) -> User:
    """
    Get the current user from the token
    if the user does not exist, create it.

    :param token: User data from the token
    :returns: User object with the same id as in the token
    """

    if tg_data is None:
        raise AuthRequired()

    (is_valid, user_data, auth_date) = validate_tg_data(tg_data, settings.tg_secret_key_bytes)

    if not is_valid:
        raise InvalidToken()

    data_json = json.loads(user_data)

    async with session.begin():
        user = await user_repository.get_user_or_none_by_id(data_json["id"])
    

    # if user.last_check is older than 5 minutes, update the user data
    if datetime.utcnow().timestamp() - user.last_check_in.timestamp() > 300:
        async with session.begin():
            user.joined = await is_member_of(request.app.state.stat_bot, COMMUNITY_TID, user.id)
            user.last_check_in = datetime.utcnow()
            await user_repository.add_user(user)
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
