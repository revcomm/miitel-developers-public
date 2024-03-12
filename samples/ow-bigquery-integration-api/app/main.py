import logging
import os
from typing import Mapping

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import HTMLResponse, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from mangum import Mangum

from app import exception_handler
from app.api.main import router as api_router
from app.log import init_app as init_log
from app.settings import Settings

settings = Settings()
app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix="/api")

# 例外ハンドラの登録
exception_handler.init_app(app)

# このアプリケーションのログ設定
init_log("app", os.environ["LOG_LEVEL"])


@app.get("/api", include_in_schema=False)
@app.get("/api/health", include_in_schema=False)
def health() -> JSONResponse:
    """ヘルスチェック"""
    return JSONResponse({"message": "It worked!!"})


@app.get("/openapi/docs", include_in_schema=False)
async def get_documentation() -> HTMLResponse:
    return get_swagger_ui_html(openapi_url="/openapi/openapi.json", title="docs")


@app.get("/openapi/openapi.json", include_in_schema=False)
async def get_open_api_endpoint() -> JSONResponse:
    return JSONResponse(get_openapi(title="FastAPI Template", version="1", routes=app.routes))


handler = Mangum(app, "off")  # FastAPIのインスタンスをMangumのコンストラクタに渡して、handlerとして読めるようにしておく
