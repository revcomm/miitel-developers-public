import json
import logging

import requests
from app.api.v1.gpt_custom.schema import OutgoingWebhookPayload
from app.router import APIRouter
from app.settings import Settings
from boto3.session import Session
from fastapi import Depends, Request
from fastapi.responses import PlainTextResponse

logger = logging.getLogger(__name__)
settings = Settings()

router = APIRouter(prefix="/v1/gpt-custom", tags=["gpt_custom"])


@router.post("/add")
async def add(request: Request, data: OutgoingWebhookPayload):
    if data.challenge:
        # ヘッダーを {'Content-Type':'text/plain'} とした 200 レスポンスで 'hex_token' 値を返す
        return PlainTextResponse(data.challenge, status_code=200)

    phrases = []
    for detail in data.call.details:
        for phrase in detail.phrases:
            for row in phrase.raw:
                phrases.append(
                    {
                        "id": str(data.call.id),
                        "tenant_code": data.call.tenant_code,
                        "dial_starts_at": detail.dial_starts_at.replace(tzinfo=None).isoformat(),
                        "order": row.order,
                        "phrase": row.phrase,
                        "phrase_nofiller": row.phrase_nofiller,
                        "starts_at": row.starts_at,
                        "ends_at": row.ends_at,
                        "filler_num": row.filler_num,
                    },
                )
    tel_number = data.call.details[0].to_number
    session = Session()
    sqs = session.client("sqs")
    body = {
        "phrases": phrases,
        "tel_number": tel_number,
    }
    sqs.send_message(
        QueueUrl=f"https://sqs.ap-northeast-1.amazonaws.com/{settings.AWS_ACCOUNT_ID}/chatgpt-serverless-sqs",
        DelaySeconds=0,
        MessageBody=(json.dumps(body)),
    )

    return {"message": "Hello World"}
