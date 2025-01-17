from aiogram import Bot, Dispatcher, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)
from aiogram.client.default import DefaultBotProperties

from src.bot.callbacks import LanguageCallback
from src.bot.handlers.lang import lang_handler
from src.bot.handlers.language import language_handler
from src.bot.handlers.raw import raw_handler
from src.bot.handlers.start import start_handler
from src.settings import get_settings

settings = get_settings()

def register_handlers(router: Router) -> None:

    router.message.register(start_handler, Command("start"))
    router.message.register(language_handler, Command("lang"))
    router.callback_query.register(lang_handler, LanguageCallback.filter())
    router.message.register(raw_handler, F.content_type.in_(["photo", "video", "document"]))


async def start_application(
    session_factory: async_sessionmaker[AsyncSession],
    stat_bot: Bot,
) -> tuple[Dispatcher, Bot]:
    # ... and all other routers should be attached to Dispatcher

    # Register startup hook to initialize webhook
    bot = Bot(settings.tg_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(session_factory=session_factory, stat_bot=stat_bot)
    router = Router()
    register_handlers(router)
    dp.include_router(router)
    await bot.set_webhook(
        settings.tg_webhook_url,
        secret_token=settings.tg_wh_secret,
    )
    return dp, bot


async def end_application(bot: Bot) -> None:
    """Stop the application."""
    await bot.session.close()
