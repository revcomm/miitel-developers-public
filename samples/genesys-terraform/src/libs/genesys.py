import boto3
import requests
import os
import json
from requests.auth import HTTPBasicAuth


class Genesys:
    @staticmethod
    def get_credentials():
        """
        シークレットマネージャーからGenesys CloudのクライアントIDとクライアントシークレットを取得

        Retrieve Genesys Cloud client ID and client secret from Secrets Manager
        """
        secret_name = "GENESYS_CLOUD_CREDENTIALS"
        client = boto3.client("secretsmanager")
        try:
            credentials = client.get_secret_value(SecretId=secret_name)
        except Exception as e:
            print(f"Error retrieving secret: {e}")
            raise e
        secret = credentials["SecretString"]
        secret_dict = json.loads(secret)
        return secret_dict["client_id"], secret_dict["client_secret"]

    @staticmethod
    def get_genesys_access_token(client_id, client_secret):
        """
        Genesys Cloudのアクセストークンを取得

        Retrieve Genesys Cloud access token
        """
        TOKEN_URL = os.getenv("GENESYS_CLOUD_TOKEN_URL")
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"grant_type": "client_credentials"}
        try:
            response = requests.post(
                TOKEN_URL,
                headers=headers,
                data=data,
                auth=HTTPBasicAuth(client_id, client_secret),
            )
            response.raise_for_status()
        except Exception as e:
            print(f"Error obtaining access token: {e}")
            raise e
        access_token = response.json().get("access_token")
        return access_token

    @staticmethod
    def get_genesys_audio_meta_data(bucket_name, object_key):
        """
        Genesys Cloudの音声ファイルのメタデータをS3から取得

        Retrieve metadata of Genesys Cloud audio files from S3
        """
        s3_client = boto3.client("s3")
        try:
            response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
            body = response["Body"].read()
            data = json.loads(body.decode("utf-8"))
            print(f"audio metadata: {data}")
            return data
        except Exception as e:
            print(f"Error getting metadata for s3://{bucket_name}/{object_key}: {e}")
            raise e

    @staticmethod
    def get_genesys_conversation_data(conversation_id, genesys_access_token):
        """
        https://developer.genesys.cloud/devapps/api-explorer#get-api-v2-analytics-conversations--conversationId--details
        """
        api_url = f"https://api.mypurecloud.jp/api/v2/analytics/conversations/{conversation_id}/details"
        headers = {"Authorization": f"Bearer {genesys_access_token}"}
        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            print(f"genesys api response: {response.json()}")
            return response.json()
        except Exception as e:
            print(f"Error getting conversation data from Genesys Cloud API: {e}")
            raise e
