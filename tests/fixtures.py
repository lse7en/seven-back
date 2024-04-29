from typing import AsyncGenerator
from fastapi import Request
import pytest_asyncio
import pytest
from unittest.mock import AsyncMock, Mock
from fastapi import FastAPI
from src.models.user import User
from src.core.database import DBSession
from repositories.user import UserRepository
from repositories.room import MovieRepository
from src.repositories.movie_import_repository import MovieImportRepository
from src.services.queue_service import QueueService
from src.services.omdb_service import OmdbService
from src.settings import Settings
from collections.abc import Generator
from unittest import mock
from src.app_api import create_application as api_create_application
from src.app_worker import create_application as worker_create_application
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from src.core.database import _get_db_session
from sqlalchemy.pool import StaticPool
from src.core.model import Base


@pytest.fixture
def mock_session():
    return AsyncMock(spec=DBSession)


@pytest_asyncio.fixture
async def mock_user():
    return AsyncMock(spec=User)


@pytest.fixture
def mock_user_repository():
    return Mock(spec=UserRepository)


@pytest.fixture
def mock_movie_repository():
    return Mock(spec=MovieRepository)


@pytest.fixture
def mock_movie_import_repository():
    return AsyncMock(spec=MovieImportRepository)


@pytest.fixture
def mock_queue_service():
    return Mock(spec=QueueService)


@pytest.fixture
def mock_omdb_service():
    return Mock(spec=OmdbService)


@pytest.fixture
def mock_settings():
    settings = Settings(
        jwt_secret="test_secret",
        jwt_exp=5,
        jwt_alg="HS256",
        google_project_id="test_project",
        omdb_api_key="omdb_api_key",
    )
    return settings


@pytest_asyncio.fixture
def gcp_pubsub_client() -> Generator:
    with mock.patch("google.cloud.pubsub_v1.PublisherClient") as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def get_db_session_overrider():
    SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite://"

    engine = create_async_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = async_sessionmaker(
        autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async def override_get_db_session(
        request: Request,
    ) -> AsyncGenerator[AsyncSession, None]:
        """
        Create and get database session.

        :param request: current request.
        :yield: database session.
        """
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            await db.commit()
            await db.close()

    return override_get_db_session


@pytest.fixture(scope="session")
def worker_app() -> Generator:
    app = worker_create_application()
    yield app


@pytest.fixture(scope="session")
def api_app() -> Generator:
    app = api_create_application()
    yield app


@pytest_asyncio.fixture(scope="function")
def api_client(
    get_db_session_overrider,
    api_app: FastAPI,
    worker_app: FastAPI,
) -> Generator:
    worker_app.dependency_overrides[_get_db_session] = get_db_session_overrider
    worker_client = TestClient(worker_app)

    class QueueServiceMock:
        def __init__(self):
            pass

        def publish_on_fetch_topic(self, *, message: str = "", **attrs) -> str:
            body = {
                "message": {
                    "data": "",
                    "messageId": attrs["movie_import_id"],
                    "attributes": attrs,
                }
            }
            worker_client.post("/movies/fetch", json=body)

    api_app.dependency_overrides[QueueService] = QueueServiceMock
    api_app.dependency_overrides[_get_db_session] = get_db_session_overrider

    api_client = TestClient(api_app)
    yield api_client
