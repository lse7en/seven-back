from typing import Annotated

from fastapi import Depends

from src.models.user import User as UserModel
from src.repositories.user_repository import UserRepository
from src.core.database import DBSession


# class UserService:
#     def __init__(
#         self, session: DBSession, user_repository: Annotated[UserRepository, Depends()]
#     ):
#         self.session = session
#         self.user_repository = user_repository


#     async def get_user_by_telegram_id(self, telegram_id: int) -> UserModel:
#         user = await self.user_repository.get_user_or_none_by_telegram_id(telegram_id)
#         # if user is None:
#         #     raise ValueError("User not found")
#         return user


#     async def get_or_create_user(self, user_data: dict, auth_data: int, ref_id: int | None) -> UserModel:
#         telegram_id = user_data.pop("id", None)
#         user = await self.user_repository.get_user_or_none_by_telegram_id(telegram_id)
#         if user is not None:
#             return user

#         else:
#             # await self.chat_service.send_admin_message(
#             #     f"New user: @{user_data.get('username', None)}, {user_data['first_name']} {user_data.get('last_name', None)}"
#             # )
#             user = UserModel(
#                 **user_data,
#                 telegram_id=telegram_id,
#                 invited_by
#             )
#         await self.user_repository.add_user(user)
#         return user


#     async def get_user(self, user_id: int) -> UserModel:
#         user = await self.user_repository.get_user_or_none_by_id(user_id)
#         return user