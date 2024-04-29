from aiogram.filters.callback_data import CallbackData
from src.bot.constants import COMMUNITY_TID

class JoinedCallback(CallbackData, prefix="joined"):
    tid: str


community_callback = JoinedCallback(tid=COMMUNITY_TID)
