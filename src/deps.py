import json
from typing import Annotated

from fastapi import Depends, Header, Request, Cookie
from aiogram import Dispatcher, Bot

from src.core.database import DBSession
from src.core.exceptions import AuthRequired, InvalidToken
from src.core.security import validate_tg_data
from src.models.user import User
from src.settings import Settings, get_settings

SettingsDep = Annotated[Settings, Depends(get_settings)]


async def get_tg_dp(request: Request) -> Dispatcher:
    return request.app.state.dp

async def get_tg_bot(request: Request) -> Bot:
    return request.app.state.bot


TGDispatcherDep = Annotated[Dispatcher, Depends(get_tg_dp)]

TGBotDep = Annotated[None, Depends(get_tg_bot)]

# async def get_current_user(
#     settings: SettingsDep,
#     session: DBSession,
#     user_service: Annotated[UserService, Depends()],
#     tg_data: Annotated[str | None, Header()] = None,
#     tg_data_cookie: Annotated[str | None, Cookie(alias='tg-data')] = None,
# ) -> User:
#     """
#     Get the current user from the token
#     if the user does not exist, create it.

#     :param token: User data from the token
#     :returns: User object with the same id as in the token
#     """

#     tg_data = tg_data or tg_data_cookie

#     if tg_data is None:
#         raise AuthRequired()

#     (is_valid, user_data, auth_date) = validate_tg_data(tg_data, settings.tg_secret_key_bytes)

#     if not is_valid:
#         raise InvalidToken()

#     data_json = json.loads(user_data)
#     async with session.begin():
#         return await user_service.get_or_create_user(data_json, auth_date)


# CurrentUser = Annotated[User, Depends(get_current_user)]
