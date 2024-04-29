from aiogram.types import Message
from src.bot.permissions import HasPermissions

HasPermissions(0)
async def raw_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    json = message.model_dump_json()
    await message.answer(json)
