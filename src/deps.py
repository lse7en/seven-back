
from typing import Annotated

from fastapi import Depends, Header, Request
from aiogram.utils.web_app import safe_parse_webapp_init_data, parse_webapp_init_data
from src.bot.constants import COMMUNITY_TID
from src.bot.validators import is_member_of
from src.core.database import DBSession
from src.core.exceptions import AuthRequired, InvalidToken
from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.settings import Settings, get_settings
from datetime import datetime, UTC, timedelta
from aiogram.utils.deep_linking import decode_payload

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
    
  # application/x-www-form-urlencoded
    try:
        data = safe_parse_webapp_init_data(token=settings.tg_token, init_data=tg_data)
        # data = parse_webapp_init_data(tg_data)
    except ValueError:
        raise InvalidToken()

    async with session.begin():
        user = await user_repository.get_user_or_none_by_id(data.user.id)
        if user is not None:
            #if user.last_check is older than 5 minutes, update the user data
            if (datetime.now(UTC).timestamp() - user.last_check_in.timestamp()) > 6000:
                print("run last check join")
                user.joined = await is_member_of(request.app.state.stat_bot, COMMUNITY_TID, user.id)
                user.last_check_in = datetime.now(UTC)
                await user_repository.add_user(user)
            return user


        try:
            ref = int(decode_payload(data.start_param)) if data.start_param else None
            referrer = await user_repository.get_user_or_none_by_id(ref)
            if referrer is None:
                ref = None
        except Exception as e:
            ref = None


        new_user = User(
                id=data.user.id,
                referrer_id=ref,
                first_name=data.user.first_name,
                last_name=data.user.last_name,
                username=data.user.username,
                joined=False,
                last_lucky_push=datetime.now(UTC) - timedelta(days=1),
                last_check_in=datetime.now(UTC)
        )
        await user_repository.add_user(new_user)

        return new_user

CurrentUser = Annotated[User, Depends(get_current_user)]
