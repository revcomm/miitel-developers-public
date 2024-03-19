from fastapi import APIRouter

from .v1.gpt_custom.views import router as gpt_custom_router

router = APIRouter()

router.include_router(gpt_custom_router)
