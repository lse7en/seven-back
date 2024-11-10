from fastapi import APIRouter

from api.endpoints import rps
from src.api.endpoints import (
    stat_webhook,
    webhook,
    profile,
    lpush,
    rank,
    secret,
    lottery,
    auth,
    adsg,
    friend_task,
)

router = APIRouter()
routers_list = (
    webhook.router,
    stat_webhook.router,
    profile.router,
    lpush.router,
    rank.router,
    secret.router,
    lottery.router,
    auth.router,
    adsg.router,
    friend_task.router,
    rps.router,
)

for r in routers_list:
    router.include_router(r)
