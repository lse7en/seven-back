from fastapi import APIRouter

from src.api.endpoints import stat_webhook, webhook

router = APIRouter()
routers_list = (webhook.router, stat_webhook.router)

for r in routers_list:
    router.include_router(r)
