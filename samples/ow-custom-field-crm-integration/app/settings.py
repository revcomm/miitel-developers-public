import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    AWS_ACCOUNT_ID: str = os.getenv("AWS_ACCOUNT_ID")
    OPEN_AI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")

    class Config:
        env = os.getenv("OW_CUSTOM_FIELD_CRM_INTEGRATION_API_ENV", "dev")
        env_file = f"envs/.env.{env}"
        case_sensitive = True


settings = Settings()
