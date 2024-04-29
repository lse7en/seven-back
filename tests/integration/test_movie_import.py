import pytest
from fastapi.testclient import TestClient

from src.schemas.movie_import_schema import MovieImportCreate


@pytest.mark.asyncio
async def test_import_movie(api_client: TestClient) -> MovieImportCreate:
    movie = MovieImportCreate(title="The Matrix")
    response = api_client.post("/api/imports", json=movie.model_dump())
    assert response.status_code == 201
    res = response.json()
    assert res["title"] == movie.title
    assert res["status"] == "fetching"

    return movie


@pytest.mark.asyncio
async def test_import_movie_with_exists_import(api_client: TestClient) -> None:
    movie = await test_import_movie(api_client)

    response = api_client.post("/api/imports", json=movie.model_dump())
    assert response.status_code == 400
