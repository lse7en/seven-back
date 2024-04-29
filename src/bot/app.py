from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from src.bot.handlers.router import router
from src.settings import get_settings

settings = get_settings()


async def start_application(
    session_factory: async_sessionmaker[AsyncSession],
) -> tuple[Dispatcher, Bot]:
    # ... and all other routers should be attached to Dispatcher

    # Register startup hook to initialize webhook
    bot = Bot(settings.tg_token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(session_factory=session_factory)

    dp.include_router(router)
    await bot.set_webhook(
        settings.tg_webhook_url,
        secret_token=settings.tg_wh_secret,
    )
    return dp, bot


async def end_application(bot: Bot) -> None:
    """Stop the application."""
    await bot.session.close()
