import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    GOOGLE_CREDENTIAL: str
    GCP_TABLE_NAME: str

    class Config:
        env = os.getenv("OW_BIGQUERY_INTEGRATION_API_ENV", "dev")
        env_file = f"envs/.env.{env}"
        case_sensitive = True
