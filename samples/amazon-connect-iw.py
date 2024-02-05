import os
from typing import Optional
from uuid import uuid4

import boto3
import requests

from datetime import datetime

s3 = boto3.resource("s3")

WEBHOOK_URL = os.environ["WEBHOOK_URL"]
USER_ID = os.environ["USER_ID"]
S3_BUCKET = os.environ["S3_BUCKET"]
INSTANCE_NAME = os.environ["INSTANCE_NAME"]


def download_recording(bucket: str, key: str):
    filename = f"/tmp/{uuid4()}.wav"
    s3 = boto3.resource("s3")
    s3.meta.client.download_file(bucket, key, filename)
    return filename


def upload_recording(url: str, filename):
    with open(filename, "rb") as f:
        response = requests.put(
            url,
            headers={"Content-Type": "audio/wav"},
            data=f,
        )
    response.raise_for_status()
    os.remove(filename)


def get_recording_object_key(contact_id: str, disconnectTimestamp: str):
    disconnect_datetime = datetime.fromisoformat(disconnectTimestamp.rstrip("Z"))
    year = disconnect_datetime.year
    month = str(disconnect_datetime.month).zfill(2)
    day = str(disconnect_datetime.day).zfill(2)

    # NOTE: 環境によっては、"connect", "CallRecordings" のパスが異なる場合があるので、適宜修正してください
    prefix = f"connect/{INSTANCE_NAME}/CallRecordings/{year}/{month}/{day}/{contact_id}"
    print("searching by prefix: " + prefix)
    res = s3.meta.client.list_objects_v2(Bucket=S3_BUCKET, Prefix=prefix)
    if not res.get("Contents"):
        raise ValueError(f"No recording found for contact {contact_id}")
    return res["Contents"][0]["Key"]


def create_call_history(
    event: dict,
    agent_number: str,
    customer_number: str,
    contact_id: str,
) -> Optional[str]:
    method = event["initiationMethod"]
    payload = {
        "call_data": [
            {
                "audio_file_type": "wav",
                "event_type": (
                    "OUTGOING_CALL" if method == "OUTBOUND" else "INCOMING_CALL"
                ),
                "call_data_id": contact_id,
                "group_name": None,
                "queue_name": None,
                "call_starts_at": event["initiationTimestamp"],
                "call_answered_at": event["agentInfo"]["connectedToAgentTimestamp"],
                "call_ends_at": event["disconnectTimestamp"],
                "participants": [
                    {
                        "type": "FROM" if method == "OUTBOUND" else "TO",
                        "miitel_user_id": USER_ID,
                        "number": agent_number,
                        "name": None,
                        "stereo_lr": "right",
                    },
                    {
                        "type": "TO" if method == "OUTBOUND" else "FROM",
                        "miitel_user_id": None,
                        "number": customer_number,
                        "name": None,
                        "stereo_lr": "left",
                    },
                ],
                "circuit_number": agent_number,
            },
        ]
    }
    headers = {"accept": "application/json", "content-type": "application/json"}

    response = requests.post(WEBHOOK_URL, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()


def lambda_handler(event, context):
    detail = event["detail"]
    contact_id = detail["contactId"]
    agent_number = detail["tags"]["aws:connect:systemEndpoint"]
    customer_number = detail["tags"]["customerNumber"]
    disconnect_timestamp = detail["disconnectTimestamp"]
    recording_object_key = get_recording_object_key(contact_id, disconnect_timestamp)
    recording_filename = download_recording(S3_BUCKET, recording_object_key)

    call_history = create_call_history(
        detail, agent_number, customer_number, contact_id
    )
    upload_url = call_history["audio_upload_urls"][0][str(contact_id)]["url"]
    upload_recording(upload_url, recording_filename)

    return {
        "statusCode": 200,
    }
