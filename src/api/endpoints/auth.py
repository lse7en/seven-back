# from typing import Annotated
# from fastapi import APIRouter, Depends, Request

# from src.core.database import DBSession
# from src.deps import SettingsDep
# from src.schemas.user_schemas import User, UserBase
# from src.repositories.user_repository import UserRepository
# from src.bot.validators import is_member_of
# from src.bot.constants import COMMUNITY_TID, FRIEND_INVITE_FILE_ID
# from src.bot.text import get_text
# from aiogram.utils import formatting
# from aiogram.utils.deep_linking import decode_payload

# from aiogram.utils.web_app import safe_parse_webapp_init_data, WebAppInitData
# from src.core.exceptions import InvalidToken
# from datetime import datetime, UTC, timedelta
# import jwt

# router = APIRouter(prefix="/auth", tags=["auth"])


# def create_access_token(
#     id: int,
#     settings: SettingsDep,
# ) -> str:
#     to_encode = {"sub": id}

#     expire = datetime.now(UTC) + timedelta(minutes=120)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
#     return encoded_jwt


# async def get_tg_data(request: Request, settings: SettingsDep) -> WebAppInitData:
#         # get tg_data from the request body
#     tg_data = (await request.json()).get("tg_data")

#     try:
#         data = safe_parse_webapp_init_data(token=settings.tg_token, init_data=tg_data)
#     except ValueError:
#         raise InvalidToken()
    
#     return data



# @router.post("", response_model=User)
# async def auth(
#     init_data: Annotated[WebAppInitData, Depends(get_tg_data)],
#     request: Request,
#     settings: SettingsDep,
#     session: DBSession,
#     user_repository: Annotated[UserRepository, Depends()],
# ):

    
#     async with session.begin():
#         user = await user_repository.get_user_for_update(init_data.user.id)
#         if user is not None:
#             #if user.last_check is older than 5 minutes, update the user data
#             if (datetime.now(UTC).timestamp() - user.last_check_in.timestamp()) > 6000:
#                 print("run last check join")
#                 user.joined = await is_member_of(request.app.state.stat_bot, COMMUNITY_TID, user.id)
#                 user.last_check_in = datetime.now(UTC)
#                 await user_repository.add_user(user)
#             return user


#         try:
#             ref = int(decode_payload(init_data.start_param)) if init_data.start_param else None
#             referrer = await user_repository.get_user_or_none_by_id(ref)
#             if referrer is None:
#                 ref = None
#         except Exception as e:
#             ref = None


#         new_user = User(
#                 id=data.user.id,
#                 referrer_id=ref,
#                 first_name=data.user.first_name,
#                 last_name=data.user.last_name,
#                 username=data.user.username,
#                 joined=False,
#                 last_lucky_push=datetime.now(UTC) - timedelta(days=1),
#                 last_check_in=datetime.now(UTC)
#         )
#         await user_repository.add_user(new_user)

#         return new_user

#     access_token_expires = timedelta(minutes=120)
#     access_token = create_access_token(
#         data={"sub": data.user.id},
#         expires_delta=access_token_expires,
#         secret_key=settings.jwt_secret_key,
#         algorithm=settings.jwt_algorithm,
#     )
#     return {"access_token": access_token, "token_type": "bearer"}
