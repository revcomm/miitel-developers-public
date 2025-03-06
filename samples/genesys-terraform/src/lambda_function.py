import urllib.parse

from call import IncomingCall, OutgoingCall, Voicemail
from libs.genesys import Genesys

client_id = None
client_secret = None


def lambda_handler(event, context):
    global client_id, client_secret

    # S3イベントからファイルのキーを取得する / Retrieve the file key from the S3 event
    for record in event["Records"]:
        bucket_name = record["s3"]["bucket"]["name"]
        object_key = record["s3"]["object"]["key"]

        # URLエンコードされた文字列をデコード / Decode the URL-encoded string
        object_key = urllib.parse.unquote(object_key)

        # Genesys CloudのクライアントIDとクライアントシークレットをシークレットマネージャーから取得 / Retrieve Genesys Cloud client ID and client secret from Secrets Manager
        if client_id is None and client_secret is None:
            client_id, client_secret = Genesys.get_credentials()

        # Genesys Cloudのアクセストークンを取得するためのリクエスト / Request to retrieve Genesys Cloud access token
        genesys_access_token = Genesys.get_genesys_access_token(
            client_id, client_secret
        )

        # Genesys Cloudの音声ファイルのメタデータを取得 / Retrieve metadata of Genesys Cloud audio files
        genesys_audio_meta_data = Genesys.get_genesys_audio_meta_data(
            bucket_name, object_key
        )

        # Incoming Webhookに送信するペイロードを作成するため、メタデータに不足している情報をGenesysのAPIから取得 / Retrieve missing information from Genesys API to create the payload for the incoming webhook
        conversation_id = genesys_audio_meta_data["conversationId"]
        genesys_conversation_data = Genesys.get_genesys_conversation_data(
            conversation_id, genesys_access_token
        )
        # Genesysの通話履歴データと音声ファイルのメタデータを基にincoming webhookへの送信を行う / Send to the incoming webhook based on Genesys call history data and audio file metadata
        result = create_call(
            genesys_conversation_data, bucket_name, genesys_audio_meta_data
        )

        return result


def create_call(genesys_conversation_data, bucket_name, genesys_audio_meta_data):
    """
    Genesys Cloudの通話履歴データから通話種別を判別し、incoming webhookに送信する関数

    Function to determine the call type from Genesys Cloud call history data and send it to the incoming webhook
    """
    incoming_call = IncomingCall.create_call(
        genesys_conversation_data, bucket_name, genesys_audio_meta_data
    )
    if incoming_call:
        return {
            "statusCode": 200,
            "body": "incoming_call history created",
        }

    outgoing_call = OutgoingCall.create_call(
        genesys_conversation_data, bucket_name, genesys_audio_meta_data
    )
    if outgoing_call:
        return {
            "statusCode": 200,
            "body": "outgoing_call history created",
        }

    voice_mail = Voicemail.create_call(
        genesys_conversation_data, bucket_name, genesys_audio_meta_data
    )
    if voice_mail:
        return {
            "statusCode": 200,
            "body": "voicemail history created",
        }

    return {
        "statusCode": 400,
        "body": "Bad Request",
    }
