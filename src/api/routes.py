from fastapi import APIRouter

from src.api.endpoints import stat_webhook, webhook, profile, lpush, rank, secret

router = APIRouter()
routers_list = (webhook.router, stat_webhook.router, profile.router, lpush.router, rank.router, secret.router)

for r in routers_list:
    router.include_router(r)
