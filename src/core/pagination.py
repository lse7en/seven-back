from fastapi import Query
from fastapi_pagination import LimitOffsetPage as BaseLimitOffsetPage

LimitOffsetPage = BaseLimitOffsetPage.with_custom_options(
    limit=Query(10, ge=1, le=100, description="Page size limit"),
)
