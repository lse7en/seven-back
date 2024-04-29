import pytest
from tests.factories import UserModelFactory
from src.core.exceptions import InvalidCredentials
from src.services.auth_service import AuthService


@pytest.mark.asyncio
async def test_authenticate_user_valid_credentials(mock_settings, mock_user_repository):
    auth_service = AuthService(
        user_repository=mock_user_repository, settings=mock_settings
    )
    password = "test_password"
    user = UserModelFactory.build(password=password)
    mock_user_repository.get_user_or_none_by_username.return_value = user
    result = await auth_service.authenticate_user(user.username, password)
    assert result == user


@pytest.mark.asyncio
async def test_authenticate_user_with_invalid_username(
    mock_settings, mock_user_repository
):
    auth_service = AuthService(
        user_repository=mock_user_repository, settings=mock_settings
    )

    user = UserModelFactory.build()
    mock_user_repository.get_user_or_none_by_username.return_value = None

    with pytest.raises(InvalidCredentials):
        await auth_service.authenticate_user(user.username, "password")


@pytest.mark.asyncio
async def test_authenticate_user_with_invalid_password(
    mock_settings, mock_user_repository
):
    auth_service = AuthService(
        user_repository=mock_user_repository, settings=mock_settings
    )

    password = "test_password"
    user = UserModelFactory.build(password=password)
    mock_user_repository.get_user_or_none_by_username.return_value = user

    with pytest.raises(InvalidCredentials):
        await auth_service.authenticate_user(user.username, "invalid_password")


@pytest.mark.asyncio
async def test_login(mock_user_repository, mock_settings):
    auth_service = AuthService(
        user_repository=mock_user_repository, settings=mock_settings
    )
    password = "test_password"
    user = UserModelFactory.build(password=password)
    mock_user_repository.get_user_or_none_by_username.return_value = user

    result = await auth_service.login(user.username, password)

    assert isinstance(result, str)
    assert len(result) > 0
