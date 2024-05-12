from aiogram import Router
from aiogram.filters import Command
from aiogram import F

from src.bot.handlers.start import start_handler
from src.bot.handlers.stat import stat_handler
from src.bot.handlers.invite import invite_handler
from src.bot.handlers.raw import raw_handler
from src.bot.handlers.join import joined_handler
from src.bot.handlers.score import score_handler
from src.bot.handlers.lang import lang_handler
from src.bot.handlers.language import language_handler
from src.bot.callbacks import JoinedCallback, LanguageCallback
router = Router()

router.message.register(start_handler, Command("start"))
router.message.register(stat_handler, Command("stat"))
router.message.register(invite_handler, Command("invite"))
router.message.register(score_handler, Command("score"))
router.message.register(language_handler, Command("lang"))
router.callback_query.register(joined_handler, JoinedCallback.filter())
router.callback_query.register(lang_handler, LanguageCallback.filter())
router.message.register(raw_handler, F.content_type.in_(["photo", "video", "document"]))