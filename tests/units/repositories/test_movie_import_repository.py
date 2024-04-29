import pytest
from unittest.mock import AsyncMock, Mock
from src.repositories.movie_import_repository import MovieImportRepository


@pytest.mark.asyncio
async def test_add_movie_import(mock_session):
    movie_import_repository = MovieImportRepository(mock_session)
    mock_session.add = Mock()
    mock_session.flush = AsyncMock()
    mock_movie_import = Mock()
    await movie_import_repository.add_movie_import(mock_movie_import)
    mock_session.add.assert_called_once_with(mock_movie_import)
    mock_session.flush.assert_called_once()


@pytest.mark.asyncio
async def test_exists_movie_import_by_title(mock_session):
    movie_import_repository = MovieImportRepository(mock_session)
    mock_session.execute = AsyncMock(return_value=Mock(scalar=Mock(return_value=True)))
    result = await movie_import_repository.exists_movie_import_by_title("test_title")
    assert result is True


@pytest.mark.asyncio
async def test_get_movie_import_or_none_by_id(mock_session):
    movie_import_repository = MovieImportRepository(mock_session)
    movie_import = Mock()
    mock_session.execute = AsyncMock(
        return_value=Mock(scalar_one_or_none=Mock(return_value=movie_import))
    )
    result = await movie_import_repository.get_movie_import_or_none_by_id(1)
    assert result == movie_import


@pytest.mark.asyncio
async def test_get_movie_or_none_by_title(mock_session):
    movie_import_repository = MovieImportRepository(mock_session)
    movie_import = Mock()
    mock_session.execute = AsyncMock(
        return_value=Mock(scalar_one_or_none=Mock(return_value=movie_import))
    )
    result = await movie_import_repository.get_movie_or_none_by_title("test_title")
    assert result == movie_import


@pytest.mark.asyncio
async def test_delete_movie(mock_session):
    movie_import_repository = MovieImportRepository(mock_session)
    mock_session.delete = AsyncMock()
    mock_movie_import = Mock()
    await movie_import_repository.delete_movie(mock_movie_import)
    mock_session.delete.assert_called_once_with(mock_movie_import)
