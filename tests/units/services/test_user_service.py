import pytest
from services.users import UserService
from schemas.user_schemas import UserCreate
from src.core.exceptions import UsernameTaken
from tests.factories import UserModelFactory


@pytest.mark.asyncio
async def test_create_user_with_new_username(mock_user_repository):
    user_service = UserService(user_repository=mock_user_repository)
    user_create = UserCreate(username="new_user", password="password")
    mock_user_repository.get_user_or_none_by_username.return_value = None

    user = await user_service.create_user(user_create)

    assert user.username == user_create.username
    mock_user_repository.add_user.assert_called_once()


@pytest.mark.asyncio
async def test_create_user_with_taken_username(mock_user_repository):
    user_service = UserService(user_repository=mock_user_repository)
    user_create = UserCreate(username="taken_user", password="password")
    old_user = UserModelFactory.build(username=user_create.username)
    mock_user_repository.get_user_or_none_by_username.return_value = old_user
    with pytest.raises(UsernameTaken):
        await user_service.create_user(user_create)

    mock_user_repository.add_user.assert_not_called()


@pytest.mark.asyncio
async def test_get_user_by_id_with_existing_id(mock_user_repository):
    user_service = UserService(user_repository=mock_user_repository)
    user = UserModelFactory.build(id=1)
    mock_user_repository.get_user_or_none_by_id.return_value = user

    result = await user_service.get_user_by_id(user.id)

    assert result == user


@pytest.mark.asyncio
async def test_get_user_by_id_with_non_existing_id(mock_user_repository):
    user_service = UserService(user_repository=mock_user_repository)
    mock_user_repository.get_user_or_none_by_id.return_value = None

    result = await user_service.get_user_by_id(999)

    assert result is None
