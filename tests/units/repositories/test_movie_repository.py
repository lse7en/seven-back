import pytest
from unittest.mock import AsyncMock, Mock
from repositories.room import MovieRepository


@pytest.mark.asyncio
async def test_list_movies(mock_session):
    movie_repository = MovieRepository(mock_session)
    mock_session.execute = AsyncMock(
        return_value=Mock(
            scalars=Mock(return_value=Mock(all=Mock(return_value=[Mock(), Mock()])))
        )
    )
    result = await movie_repository.list_movies(0, 10)
    mock_session.execute.assert_called_once()
    assert len(result) == 2


@pytest.mark.asyncio
async def test_add_movie(mock_session):
    movie_repository = MovieRepository(mock_session)
    mock_session.add = Mock()
    mock_session.flush = AsyncMock()
    mock_movie = Mock()
    await movie_repository.add_movie(mock_movie)
    mock_session.add.assert_called_once_with(mock_movie)
    mock_session.flush.assert_called_once()


@pytest.mark.asyncio
async def test_get_movie_or_none_by_id(mock_session):
    movie_repository = MovieRepository(mock_session)
    movie = Mock()
    mock_session.execute = AsyncMock(
        return_value=Mock(scalar_one_or_none=Mock(return_value=movie))
    )
    result = await movie_repository.get_movie_or_none_by_id(1)
    assert result == movie


@pytest.mark.asyncio
async def test_get_movie_or_none_by_title(mock_session):
    movie_repository = MovieRepository(mock_session)
    movie = Mock()
    mock_session.execute = AsyncMock(
        return_value=Mock(scalar_one_or_none=Mock(return_value=movie))
    )
    result = await movie_repository.get_movie_or_none_by_title("test_title")
    assert result == movie


@pytest.mark.asyncio
async def test_exists_movie_by_title(mock_session):
    movie_repository = MovieRepository(mock_session)
    mock_session.execute = AsyncMock(
        return_value=Mock(scalar_one=Mock(return_value=True))
    )
    result = await movie_repository.exists_movie_by_title("test_title")
    assert result is True


@pytest.mark.asyncio
async def test_delete_movie(mock_session):
    movie_repository = MovieRepository(mock_session)
    mock_session.delete = AsyncMock()
    mock_movie = Mock()
    await movie_repository.delete_movie(mock_movie)
    mock_session.delete.assert_called_once_with(mock_movie)
