
from sqlalchemy.ext.asyncio import AsyncSession


from src.repositories.user_repository import UserRepository
from src.repositories.secret_repository import SecretCodeRepository

# from src.services.users import UserService

async def get_user_repository(session: AsyncSession) -> UserRepository:
    return UserRepository(session)



async def get_secret_code_repository(session: AsyncSession) -> SecretCodeRepository:
    return SecretCodeRepository(session)


# async def get_user_service(session: AsyncSession) -> UserService:
#     return UserService(
#         session=session, user_repository=await get_user_repository(session)
#     )

