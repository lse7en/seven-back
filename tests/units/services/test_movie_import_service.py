import pytest
from unittest.mock import Mock

from tests.factories import MovieImportCreateSchemaFactory

from src.core.exceptions import MovieAlreadyExists, MovieAlreadySubmitted
from services.active_room import MovieImportService


@pytest.mark.asyncio
async def test_movie_import_service_import_movie(
    mock_movie_import_repository, mock_movie_repository, mock_queue_service
):
    movie_import_create = MovieImportCreateSchemaFactory.build()

    movie_import_service = MovieImportService(
        movie_import_repository=mock_movie_import_repository,
        movie_repository=mock_movie_repository,
        background_tasks=Mock(),
        queue_service=mock_queue_service,
    )

    mock_movie_repository.exists_movie_by_title.return_value = False
    mock_movie_import_repository.exists_movie_import_by_title.return_value = False

    result = await movie_import_service.import_movie(movie_import_create)

    assert result.title == movie_import_create.title
    assert mock_movie_import_repository.add_movie_import.called
    mock_movie_repository.exists_movie_by_title.assert_called_once_with(
        movie_import_create.title
    )
    mock_movie_import_repository.exists_movie_import_by_title.assert_called_once_with(
        movie_import_create.title
    )


@pytest.mark.asyncio
async def test_movie_import_service_import_movie_movie_already_exists(
    mock_movie_import_repository, mock_movie_repository, mock_queue_service
):
    movie_import_create = MovieImportCreateSchemaFactory.build()

    movie_import_service = MovieImportService(
        movie_import_repository=mock_movie_import_repository,
        movie_repository=mock_movie_repository,
        background_tasks=Mock(),
        queue_service=mock_queue_service,
    )

    mock_movie_repository.exists_movie_by_title.return_value = True

    with pytest.raises(MovieAlreadyExists):
        await movie_import_service.import_movie(movie_import_create)

    mock_movie_repository.exists_movie_by_title.assert_called_once_with(
        movie_import_create.title
    )


@pytest.mark.asyncio
async def test_movie_import_service_import_movie_movie_already_submitted(
    mock_movie_import_repository, mock_movie_repository, mock_queue_service
):
    movie_import_create = MovieImportCreateSchemaFactory.build()

    movie_import_service = MovieImportService(
        movie_import_repository=mock_movie_import_repository,
        movie_repository=mock_movie_repository,
        background_tasks=Mock(),
        queue_service=mock_queue_service,
    )

    mock_movie_repository.exists_movie_by_title.return_value = False
    mock_movie_import_repository.exists_movie_import_by_title.return_value = True

    with pytest.raises(MovieAlreadySubmitted):
        await movie_import_service.import_movie(movie_import_create)

    mock_movie_repository.exists_movie_by_title.assert_called_once_with(
        movie_import_create.title
    )
    mock_movie_import_repository.exists_movie_import_by_title.assert_called_once_with(
        movie_import_create.title
    )
