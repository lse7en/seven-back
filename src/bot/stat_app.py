from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)


from src.bot.handlers.stat import stat_handler
from src.settings import get_settings

settings = get_settings()

def register_handlers(router: Router) -> None:

    router.message.register(stat_handler, Command("stat"))



async def start_application(
    session_factory: async_sessionmaker[AsyncSession],
) -> tuple[Dispatcher, Bot]:
    # ... and all other routers should be attached to Dispatcher

    # Register startup hook to initialize webhook
    stat_bot = Bot(settings.stat_tg_token, parse_mode=ParseMode.HTML)
    stat_dp = Dispatcher(session_factory=session_factory)
    router = Router()
    register_handlers(router)
    stat_dp.include_router(router)
    await stat_bot.set_webhook(
        settings.stat_tg_webhook_url,
        secret_token=settings.tg_wh_secret,
    )
    return stat_dp, stat_bot


async def end_application(bot: Bot) -> None:
    """Stop the application."""
    await bot.session.close()
