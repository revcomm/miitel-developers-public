from fastapi import APIRouter

from .v1.bigquery.views import router as bigquery_router

router = APIRouter()

router.include_router(bigquery_router)
