import boto3
import os
import requests
import tempfile
import uuid

from libs.util import Utils


class IncomingWebhook:
    @staticmethod
    def create_payload(genesys_miitel_mapped_data):
        """
        Genesys CloudのsegmentデータをMiiTelのIncoming Webhookのpayloadに変換する関数

        Function to convert Genesys Cloud segment data to MiiTel's Incoming Webhook payload

        Reference: https://developer.genesys.cloud/analyticsdatamanagement/analytics/detail/conversation-data-model
        """

        payload = {"call_data": []}
        for miitel_event_type, genesys_segment in genesys_miitel_mapped_data:
            # Genesys Cloudの電話番号とMiiTelのユーザーID、ユーザー名のマッピング / Mapping of Genesys Cloud phone numbers to MiiTel user IDs and user names
            phonenumber_user_map = {
                # "genesys_phone_number": ("miitel_user_id", "miitel_user_name")
                "tel:+8180XXXXXXXX": (
                    "b7b743b6-ceb9-4324-aaf1-032902c7d521",
                    "Miitel Ichiro",
                ),
                "tel:+8150XXXXXXXX": (
                    "8783436c-79d9-4c3f-95c9-07a5ec4630d3",
                    "Miitel Jiro",
                ),
            }

            call_starts_at = genesys_segment["callStartsAt"]
            call_answered_at = genesys_segment["segmentStart"]
            call_ends_at = genesys_segment["segmentEnd"]

            from_participant_number = Utils.format_phone_number(genesys_segment["from"])
            from_miitel_user_id, from_miitel_user_name = phonenumber_user_map.get(
                genesys_segment["from"], (None, None)
            )

            to_participant_number = Utils.format_phone_number(genesys_segment["to"])
            to_miitel_user_id, to_miitel_user_name = phonenumber_user_map.get(
                genesys_segment["to"], (None, None)
            )

            # circuit_numberの設定 / Setting circuit_number
            match miitel_event_type:
                case "INCOMING_CALL":
                    circuit_number = to_participant_number
                case "OUTGOING_CALL":
                    circuit_number = from_participant_number
                case "AUTOMATIC_RECORD":
                    circuit_number = to_participant_number
                case _:
                    # NOTE: 他のイベントタイプの場合の処理を追加 / Add codes for other event types
                    circuit_number = ""

            data = {
                "call_data_id": str(uuid.uuid4()),
                "audio_file_type": "wav",
                "event_type": miitel_event_type,
                "group_name": "",
                "queue_name": "",
                "call_starts_at": call_starts_at,
                "call_answered_at": call_answered_at,
                "call_ends_at": call_ends_at,
                "circuit_number": circuit_number,
                "participants": [
                    {
                        "type": "FROM",
                        "stereo_lr": "left",
                        "miitel_user_id": from_miitel_user_id,
                        "number": from_participant_number,
                        "name": from_miitel_user_name,
                    },
                    {
                        "type": "TO",
                        "stereo_lr": "right",
                        "miitel_user_id": to_miitel_user_id,
                        "number": to_participant_number,
                        "name": to_miitel_user_name,
                    },
                ],
                "tags": [{"value": "Genesys Example"}],
            }
            payload["call_data"].append(data)
        return payload

    @staticmethod
    def post_incoming_webhook(payload):
        """
        MiiTelのIncoming Webhookを送信する関数

        Function to send MiiTel Incoming Webhook
        """
        INCOMING_WEBHOOK_ENDPOINT = os.getenv("MIITEL_INCOMING_WEBHOOK_URL")

        try:
            response = requests.post(INCOMING_WEBHOOK_ENDPOINT, json=payload)
            response.raise_for_status()
            print(f"post incoming webhook: {response.json()}")
            return response.json()["audio_upload_urls"]
        except Exception as e:
            print(f"Error in incoming webhook: {e}")
            raise e

    @staticmethod
    def upload_audio_file(audio_upload_url, bucket_name, audio_path):
        """
        音声ファイルをS3からダウンロードし、Incoming Webhookの音声アップロードURLにputする関数

        Function to download audio files from S3 and put them to the Incoming Webhook audio upload URL
        """
        for value in audio_upload_url.values():
            with tempfile.TemporaryDirectory() as tmpdir:
                download_path = os.path.join(tmpdir, f"{audio_path.split('/')[-1]}")
                try:
                    s3_client = boto3.client("s3")
                    s3_client.download_file(bucket_name, audio_path, download_path)
                    print(f"Downloaded file to {download_path}")
                except Exception as e:
                    print(f"Error downloading file from S3: {e}")
                    return False

                try:
                    with open(download_path, "rb") as file:
                        response = requests.put(value.get("url"), data=file)
                        response.raise_for_status()
                except Exception as e:
                    print(f"Error uploading file to URL: {e}")
                    return False
        return True
