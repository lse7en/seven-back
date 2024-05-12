from contextlib import asynccontextmanager
from typing import AsyncGenerator

from src.api.routes import router
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from fastapi_pagination.utils import disable_installed_extensions_check

from src.core.database import setup_db
from src.bot.bot_app import start_application, end_application
from src.bot.stat_app import start_application as start_stat_application, end_application as end_stat_application


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    # Startup 
    engine, session_factory = setup_db()
    _application.state.db_engine = engine
    _application.state.session_factory = session_factory

    stat_dp, stat_bot = await start_stat_application(session_factory=session_factory)
    dp, bot = await start_application(session_factory=session_factory, stat_bot=stat_bot)

    _application.state.dp = dp
    _application.state.bot = bot
    _application.state.stat_dp = stat_dp
    _application.state.stat_bot = stat_bot

    yield
    

    # Shutdown
    await end_application(bot)
    await end_stat_application(stat_bot)
    await engine.dispose()


def create_application() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    @app.get("/health")
    async def health_check():
        return {"status": "ok"}
    

    app.include_router(router, prefix="/api")
    add_pagination(app)
    disable_installed_extensions_check()

    return app