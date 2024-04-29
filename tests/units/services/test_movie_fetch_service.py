import pytest
from src.services.movie_fetch_service import MovieFetchService
from src.models.movie_import import ImportStatus
from tests.factories import MovieModelFactory, MovieImportModelFactory, MovieOmdbFactory


@pytest.mark.asyncio
async def test_fetch_movie_data_already_fetched(
    mock_movie_import_repository, mock_movie_repository, mock_omdb_service, mock_session
):
    movie_fetch_service = MovieFetchService(
        movie_import_repository=mock_movie_import_repository,
        movie_repository=mock_movie_repository,
        omdb_service=mock_omdb_service,
        session=mock_session,
    )

    movie_import = MovieImportModelFactory.build(status=ImportStatus.FETCHED)
    mock_movie_import_repository.get_movie_import_or_none_by_id.return_value = (
        movie_import
    )

    await movie_fetch_service.fetch_movie_data(
        movie_import_id=movie_import.id, movie_title="test_title"
    )

    mock_movie_import_repository.get_movie_import_or_none_by_id.assert_called_once_with(
        movie_import.id
    )
    mock_movie_repository.get_movie_or_none_by_title.assert_not_called()
    mock_omdb_service.get_movie_by_title.assert_not_called()


@pytest.mark.asyncio
async def test_fetch_movie_data_already_imported(
    mock_movie_import_repository, mock_movie_repository, mock_omdb_service, mock_session
):
    movie_fetch_service = MovieFetchService(
        movie_import_repository=mock_movie_import_repository,
        movie_repository=mock_movie_repository,
        omdb_service=mock_omdb_service,
        session=mock_session,
    )
    movie_import = MovieImportModelFactory.build(status=ImportStatus.FETCHING)
    mock_movie_import_repository.get_movie_import_or_none_by_id.return_value = (
        movie_import
    )

    movie = MovieModelFactory.build(title=movie_import.title)
    mock_movie_repository.get_movie_or_none_by_title.return_value = movie

    await movie_fetch_service.fetch_movie_data(
        movie_import_id=movie_import.id, movie_title=movie.title
    )

    mock_movie_import_repository.get_movie_import_or_none_by_id.assert_called_once_with(
        movie_import.id
    )
    mock_movie_repository.get_movie_or_none_by_title.assert_called_once_with(
        movie.title
    )
    mock_movie_import_repository.add_movie_import.assert_called_once_with(movie_import)
    mock_omdb_service.get_movie_by_title.assert_not_called()


@pytest.mark.asyncio
async def test_fetch_movie_data_not_found(
    mock_movie_import_repository, mock_movie_repository, mock_omdb_service, mock_session
):
    movie_fetch_service = MovieFetchService(
        movie_import_repository=mock_movie_import_repository,
        movie_repository=mock_movie_repository,
        omdb_service=mock_omdb_service,
        session=mock_session,
    )
    movie_import = MovieImportModelFactory.build(status=ImportStatus.FETCHING)
    mock_movie_import_repository.get_movie_import_or_none_by_id.return_value = (
        movie_import
    )
    mock_movie_repository.get_movie_or_none_by_title.return_value = None
    mock_omdb_service.get_movie_by_title.return_value = {"Response": "False"}

    await movie_fetch_service.fetch_movie_data(
        movie_import_id=movie_import.id, movie_title=movie_import.title
    )

    mock_movie_import_repository.get_movie_import_or_none_by_id.assert_called_once_with(
        movie_import.id
    )
    mock_movie_repository.get_movie_or_none_by_title.assert_called_once_with(
        movie_import.title
    )
    mock_omdb_service.get_movie_by_title.assert_called_once_with(movie_import.title)
    assert movie_import.status == ImportStatus.NOT_FOUND
    mock_movie_import_repository.add_movie_import.assert_called_once_with(movie_import)


@pytest.mark.asyncio
async def test_fetch_movie_data_success(
    mock_movie_import_repository, mock_movie_repository, mock_omdb_service, mock_session
):
    movie_fetch_service = MovieFetchService(
        movie_import_repository=mock_movie_import_repository,
        movie_repository=mock_movie_repository,
        omdb_service=mock_omdb_service,
        session=mock_session,
    )
    movie_import = MovieImportModelFactory.build(status=ImportStatus.FETCHING)
    mock_movie_import_repository.get_movie_import_or_none_by_id.return_value = (
        movie_import
    )
    mock_movie_repository.get_movie_or_none_by_title.return_value = None

    omdb_result = MovieOmdbFactory.build(title=movie_import.title).model_dump(
        by_alias=True
    )
    omdb_result["Response"] = "True"

    mock_omdb_service.get_movie_by_title.return_value = omdb_result
    await movie_fetch_service.fetch_movie_data(
        movie_import_id=movie_import.id, movie_title=movie_import.title
    )

    mock_movie_import_repository.get_movie_import_or_none_by_id.assert_called_once_with(
        movie_import.id
    )
    mock_movie_repository.get_movie_or_none_by_title.assert_called_once_with(
        movie_import.title
    )
    mock_omdb_service.get_movie_by_title.assert_called_once_with(movie_import.title)
    mock_movie_repository.add_movie.assert_called_once()
    mock_movie_import_repository.add_movie_import.assert_called_once()


@pytest.mark.asyncio
async def test_proccess_dead_letter(
    mock_movie_import_repository, mock_movie_repository, mock_omdb_service, mock_session
):
    movie_fetch_service = MovieFetchService(
        movie_import_repository=mock_movie_import_repository,
        movie_repository=mock_movie_repository,
        omdb_service=mock_omdb_service,
        session=mock_session,
    )
    movie_import = MovieImportModelFactory.build(status=ImportStatus.FETCHING)
    mock_movie_import_repository.get_movie_import_or_none_by_id.return_value = (
        movie_import
    )

    movie_import = await movie_fetch_service.process_dead_letter(
        movie_import_id=movie_import.id, movie_title=movie_import.title
    )

    mock_movie_import_repository.get_movie_import_or_none_by_id.assert_called_once_with(
        movie_import.id
    )
    assert movie_import.status == ImportStatus.ERROR
    mock_movie_import_repository.add_movie_import.assert_called_once_with(movie_import)
