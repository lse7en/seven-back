import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_health(api_client: TestClient) -> None:
    response = api_client.get("/health")
    assert response.status_code == 200
