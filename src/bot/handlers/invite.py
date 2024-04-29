from aiogram.types import Message
from aiogram.utils.markdown import hbold
from src.bot.permissions import IsChannelMember
from src.bot.constants import COMMUNITY_TID
from aiogram.utils import formatting
from aiogram.utils.deep_linking import create_start_link

random_string = '1234567890abcdefghijklmnopqrstuvwxyz'


 



@IsChannelMember(COMMUNITY_TID)
async def invite_handler(message: Message) -> None:

    link = await create_start_link(message.bot, payload=str(message.from_user.id), encode=True)

    caption = formatting.as_list(
    formatting.as_line(
        formatting.Bold("🌟 Join our Telegram community!"),
        "We share insights and 100% of our ad revenue with subscribers monthly. Could you be one of the winners?",
        sep="\n",
    ),
    formatting.as_line(
        "Join here:",
        formatting.Url(link),
        sep=" ",
    ),
    formatting.as_line("Let's win together! 🚀"),
    sep="\n\n",
)



    await message.answer(caption.as_html())