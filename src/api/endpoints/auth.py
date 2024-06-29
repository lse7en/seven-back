from typing import Annotated
from fastapi import APIRouter, Depends, Request

from src.core.database import DBSession
from src.deps import SettingsDep
from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.bot.validators import is_member_of
from sqlalchemy import update
from aiogram.utils.deep_linking import decode_payload
from src.bot.constants import COMMUNITY_TID
from aiogram.utils.web_app import safe_parse_webapp_init_data, WebAppInitData, parse_webapp_init_data
from src.core.exceptions import InvalidToken
from datetime import datetime, UTC, timedelta
import jwt

router = APIRouter(prefix="/auth", tags=["auth"])


def create_access_token(
    data: dict,
    expires_delta: timedelta,
    secret_key: str,
    algorithm: str,
) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt



async def get_tg_data(request: Request, settings: SettingsDep) -> WebAppInitData:
        # get tg_data from the request body
    tg_data = (await request.json()).get("tg_data")

    try:
        # data = parse_webapp_init_data(tg_data)
        data = safe_parse_webapp_init_data(token=settings.tg_token, init_data=tg_data)
    except ValueError:
        raise InvalidToken()
    
    return data




async def upsert_user(
    data: Annotated[WebAppInitData, Depends(get_tg_data)],
    request: Request,
    session: DBSession,
    user_repository: Annotated[UserRepository, Depends()],
) -> User:

    async with session.begin():
        user = await user_repository.get_user_or_none_by_id(data.user.id)
        if user is not None:
            #if user.last_check is older than 5 minutes, update the user data
            if (datetime.now(UTC).timestamp() - user.last_check_in.timestamp()) > 6000:
                print("run last check join")
                joined = await is_member_of(request.app.state.stat_bot, COMMUNITY_TID, user.id)
                last_check_in = datetime.now(UTC)

                query = update(User).where(User.id == user.id).values(joined=joined, last_check_in=last_check_in).returning(User)
                res = await session.execute(query)
                return res.scalar_one()
            return user


        try:
            ref = int(decode_payload(data.start_param)) if data.start_param else None
            # referrer = await user_repository.get_user_or_none_by_id(ref)
            # if referrer is None:
            #     ref = None
        except Exception as e:
            ref = None

        try:
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
        except Exception as e:
            print("should_not_happen", e)

        return await user_repository.get_user_or_none_by_id(data.user.id)


@router.post("")
async def auth(
    user: Annotated[User, Depends(upsert_user)],
    settings: SettingsDep,
):
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=timedelta(minutes=settings.jwt_expiration),
        secret_key=settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )
    return {"access_token": access_token, "token_type": "bearer"}
