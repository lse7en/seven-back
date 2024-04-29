import pytest
from tests.factories import UserCreateSchemaFactory
from fastapi.testclient import TestClient

from schemas.user_schemas import UserCreate
from src.core.constants import ErrorCode


@pytest.mark.asyncio
async def test_user_login_invalid(api_client: TestClient) -> None:
    user = UserCreateSchemaFactory.build()
    response = api_client.post("/api/users", json=user.model_dump())
    assert response.status_code == 201

    user2 = UserCreateSchemaFactory.build(
        username=user.username, password=user.password + "invalid"
    )
    response = api_client.post("/api/auth", json=user2.model_dump())
    assert response.status_code == 401
    res = response.json()
    assert res["detail"] == ErrorCode.INVALID_CREDENTIALS


@pytest.mark.asyncio
async def test_user_create_and_login(api_client: TestClient) -> UserCreate:
    user = UserCreateSchemaFactory.build()
    response = api_client.post("/api/users", json=user.model_dump())
    assert response.status_code == 201

    response = api_client.post("/api/auth", json=user.model_dump())
    assert response.status_code == 200
    res = response.json()
    token = res["access_token"]
    api_client.headers = {"Authorization": f"Bearer {token}"}
    return user


@pytest.mark.asyncio
async def test_get_profile(api_client):
    user = await test_user_create_and_login(api_client)

    response = api_client.get("/api/users/me")
    assert response.status_code == 200
    res = response.json()
    assert res["username"] == user.username
