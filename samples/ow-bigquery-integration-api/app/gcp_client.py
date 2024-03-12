from google.cloud import bigquery
from google.cloud.bigquery.client import Client
from google.oauth2 import service_account

from app.common import cache
from app.settings import Settings

settings = Settings()


@cache(seconds=300)
def init_bigquery_client() -> Client:
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
    credentials = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_CREDENTIAL, scopes=scopes
    )
    return bigquery.Client(credentials=credentials, project=credentials.project_id)
