import pytest
from fastapi.testclient import TestClient
from src.core.constants import ErrorCode
from src.schemas.movie_import_schema import MovieImportCreate

from tests.integration.test_movie_import import test_import_movie
from tests.integration.test_user_auth import test_user_create_and_login


@pytest.mark.asyncio
async def test_list_movie(api_client: TestClient) -> MovieImportCreate:
    movie = await test_import_movie(api_client)
    response = api_client.get("/api/movies")

    assert response.status_code == 200
    res = response.json()
    assert res["total"] == 1
    item = res["items"][0]
    assert item["title"] == movie.title


@pytest.mark.asyncio
async def test_detail_movie(api_client: TestClient) -> MovieImportCreate:
    movie = await test_import_movie(api_client)
    response = api_client.get(f"/api/movies/{movie.title}")

    assert response.status_code == 200
    res = response.json()
    assert res["title"] == movie.title


@pytest.mark.asyncio
async def test_detail_movie_not_found(api_client: TestClient) -> None:
    response = api_client.get("/api/movies/not_found")

    assert response.status_code == 404
    res = response.json()
    assert res["detail"] == ErrorCode.MOVIE_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_movie_unauthorized(api_client: TestClient) -> None:
    movie = await test_import_movie(api_client)
    response = api_client.delete(f"/api/movies/{movie.title}")

    assert response.status_code == 401
    res = response.json()
    assert res["detail"] == ErrorCode.AUTHENTICATION_REQUIRED


@pytest.mark.asyncio
async def test_delete_movie(api_client: TestClient) -> None:
    movie_create = await test_import_movie(api_client)
    await test_user_create_and_login(api_client)
    res = api_client.get(f"/api/movies/{movie_create.title}")

    assert res.status_code == 200

    movie_id = res.json()["id"]

    response = api_client.delete(f"/api/movies/{movie_id}")
    assert response.status_code == 204

    res = api_client.get(f"/api/movies/{movie_create.title}")

    assert res.status_code == 404
    res = res.json()
