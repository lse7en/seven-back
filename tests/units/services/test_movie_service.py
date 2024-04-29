import pytest
from src.services.movie_service import MovieService
from src.core.exceptions import MovieNotFound
from tests.factories import MovieModelFactory, UserModelFactory


@pytest.mark.asyncio
async def test_list_movies(mock_movie_repository):
    movie_service = MovieService(movie_repository=mock_movie_repository)
    mock_movie_repository.list_movies.return_value = [
        MovieModelFactory.build() for _ in range(5)
    ]

    result = await movie_service.list_movies(offset=0, limit=5)

    assert len(result) == 5
    mock_movie_repository.list_movies.assert_called_once_with(0, 5)


@pytest.mark.asyncio
async def test_delete_movie(mock_movie_repository):
    movie_service = MovieService(movie_repository=mock_movie_repository)
    user = UserModelFactory.build()
    movie = MovieModelFactory.build()
    mock_movie_repository.get_movie_or_none_by_id.return_value = movie

    await movie_service.delete_movie(user, movie.id)

    mock_movie_repository.get_movie_or_none_by_id.assert_called_once_with(movie.id)
    mock_movie_repository.delete_movie.assert_called_once_with(movie)


@pytest.mark.asyncio
async def test_delete_movie_not_found(mock_movie_repository):
    movie_service = MovieService(movie_repository=mock_movie_repository)
    user = UserModelFactory.build()
    mock_movie_repository.get_movie_or_none_by_id.return_value = None

    # Act & Assert
    with pytest.raises(MovieNotFound):
        await movie_service.delete_movie(user, 1)


@pytest.mark.asyncio
async def test_get_movie(mock_movie_repository):
    movie_service = MovieService(movie_repository=mock_movie_repository)
    movie = MovieModelFactory.build()
    mock_movie_repository.get_movie_or_none_by_title.return_value = movie

    result = await movie_service.get_movie(movie.title)

    assert result == movie
    mock_movie_repository.get_movie_or_none_by_title.assert_called_once_with(
        movie.title
    )


@pytest.mark.asyncio
async def test_get_movie_not_found(mock_movie_repository):
    movie_service = MovieService(movie_repository=mock_movie_repository)
    mock_movie_repository.get_movie_or_none_by_title.return_value = None

    with pytest.raises(MovieNotFound):
        await movie_service.get_movie("Nonexistent Movie")
