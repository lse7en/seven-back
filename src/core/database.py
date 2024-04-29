from typing import Annotated, AsyncGenerator
from fastapi import Depends, Request, WebSocket

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy import log as sqlalchemy_log

# Disable default logging
# sqlalchemy_log._add_default_handler = lambda x: None


def setup_db() -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    """
    Creates connection to the database.

    This function creates SQLAlchemy engine instance,
    session_factory for creating sessions
    and returns them.

    :param app: fastAPI application.
    :return: SQLAlchemy engine and session_factory.
    """
    from src.settings import get_settings

    settings = get_settings()


    engine = create_async_engine(settings.db_url, echo=settings.postgres_echo, connect_args=settings.db_connections_args)

    session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )
    return engine, session_factory


async def _get_db_session(
    request: Request = None, websocket: WebSocket = None
) -> AsyncGenerator[AsyncSession, None]:
    """
    Create and get database session.

    :param request: current request.
    :yield: database session.
    """

    app = request.app if request else websocket.app


    session: AsyncSession = app.state.session_factory()
    try:  # noqa: WPS501
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.commit()
        await session.close()


DBSession = Annotated[AsyncSession, Depends(_get_db_session)]
