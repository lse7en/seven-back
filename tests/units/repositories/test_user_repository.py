import pytest
from unittest.mock import AsyncMock, Mock

from repositories.user import UserRepository


@pytest.mark.asyncio
async def test_add_user(mock_user, mock_session):
    user_repository = UserRepository(mock_session)
    mock_session.add = Mock()
    mock_session.flush = AsyncMock()
    await user_repository.add_user(mock_user)
    mock_session.add.assert_called_once_with(mock_user)
    mock_session.flush.assert_called_once()


@pytest.mark.asyncio
async def test_get_user_or_none_by_username(mock_session):
    user_repository = UserRepository(mock_session)
    user = Mock()
    mock_session.execute = AsyncMock(
        return_value=Mock(scalar_one_or_none=Mock(return_value=user))
    )
    result = await user_repository.get_user_or_none_by_username("test_username")
    assert result == user


@pytest.mark.asyncio
async def test_get_user_or_none_by_id(mock_session):
    user_repository = UserRepository(mock_session)
    user = Mock()
    mock_session.execute = AsyncMock(
        return_value=Mock(scalar_one_or_none=Mock(return_value=user))
    )
    result = await user_repository.get_user_or_none_by_id("test_id")
    assert result == user
