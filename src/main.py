from contextlib import asynccontextmanager
from typing import AsyncGenerator
import asyncio
from src.api.routes import router
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from fastapi_pagination.utils import disable_installed_extensions_check
from src.tasks.group_logs import stat_task
from src.core.database import setup_db
from src.bot.bot_app import start_application, end_application
from src.bot.stat_app import start_application as start_stat_application, end_application as end_stat_application
from fastapi.middleware.cors import CORSMiddleware
from src.settings import get_settings

settings = get_settings()



@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    # Startup 
    engine, session_factory = setup_db()
    _application.state.db_engine = engine
    _application.state.session_factory = session_factory

    if settings.run_tg_apps:
        print("starting tg apps")
        stat_dp, stat_bot = await start_stat_application(session_factory=session_factory)
        dp, bot = await start_application(session_factory=session_factory, stat_bot=stat_bot)

        _application.state.dp = dp
        _application.state.bot = bot
        _application.state.stat_dp = stat_dp
        _application.state.stat_bot = stat_bot

        asyncio.create_task(stat_task(stat_bot, session_factory))
    yield
    

    # Shutdown
    if settings.run_tg_apps:
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
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
