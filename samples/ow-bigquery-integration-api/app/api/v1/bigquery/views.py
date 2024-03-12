import logging

from app import gcp_client as gcp
from app.router import APIRouter
from app.settings import Settings
from fastapi import Depends, Request
from fastapi.responses import PlainTextResponse

from .schema import OutgoingWebhookPayload

logger = logging.getLogger(__name__)
settings = Settings()

router = APIRouter(prefix="/v1/bigquery", tags=["bigquery"])


@router.post("/add")
async def add(request: Request, data: OutgoingWebhookPayload):
    if data.challenge:
        # ヘッダーを {'Content-Type':'text/plain'} とした 200 レスポンスで 'hex_token' 値を返す
        return PlainTextResponse(data.challenge, status_code=200)

    gcp_client = gcp.init_bigquery_client()

    rows_to_insert = []
    for detail in data.call.details:
        rows_to_insert.append(
            {
                "id": str(data.call.id),
                "tenant_code": data.call.tenant_code,
                "dial_starts_at": detail.dial_starts_at.replace(
                    tzinfo=None
                ).isoformat(),
            },
        )
    errors = gcp_client.insert_rows_json(settings.GCP_TABLE_NAME, rows_to_insert)
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))
    return {"message": "Hello World"}
