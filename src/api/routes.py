from fastapi import APIRouter

from src.api.endpoints import webhook
router = APIRouter()
routers_list = (webhook.router,)

for r in routers_list:
    router.include_router(r)
