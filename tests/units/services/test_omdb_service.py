import pytest
from src.services.omdb_service import OmdbService
from aioresponses import aioresponses


@pytest.mark.asyncio
async def test_get_movie_by_title(mock_settings):
    omdb_service = OmdbService(settings=mock_settings)

    movie_title = "test_movie"
    expected_response = {"Title": "Test Movie", "Year": "2020"}

    with aioresponses() as m:
        m.get(
            f"http://www.omdbapi.com/?t={movie_title}&apikey={mock_settings.omdb_api_key}",
            payload=expected_response,
        )

        response = await omdb_service.get_movie_by_title(title=movie_title)

        assert response == expected_response


@pytest.mark.asyncio
async def test_get_movie_by_id(mock_settings):
    omdb_service = OmdbService(settings=mock_settings)

    movie_id = "test_id"
    expected_response = {"Title": "Test Movie", "Year": "2020"}

    with aioresponses() as m:
        m.get(
            f"http://www.omdbapi.com/?i={movie_id}&apikey={mock_settings.omdb_api_key}",
            payload=expected_response,
        )

        response = await omdb_service.get_movie_by_id(movie_id=movie_id)

        assert response == expected_response
