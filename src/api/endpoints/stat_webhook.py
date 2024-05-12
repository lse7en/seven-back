from typing import Annotated

from fastapi import APIRouter, Header, Request

from src.deps import SettingsDep
from src.core.exceptions import InvalidCredentials


router = APIRouter(prefix="/stat-webhook", tags=["stat-webhook"])


@router.post("")
async def webhook(
    request: Request,
    settings: SettingsDep,
    x_telegram_bot_api_secret_token: Annotated[str | None, Header()] = None,
):
    tg_dp = request.app.state.stat_dp
    tg_bot = request.app.state.stat_bot
    if x_telegram_bot_api_secret_token != settings.tg_wh_secret:
        raise InvalidCredentials()
    await tg_dp.feed_webhook_update(tg_bot, await request.json())
