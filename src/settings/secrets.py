import os
from pathlib import Path
from typing import Optional

from pydantic import field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_DIR = Path(__file__).resolve().parents[2]
ENV_FILE_PATH = os.path.join(PROJECT_DIR, ".env")


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH, case_sensitive=True)


class Secrets(BaseConfig):

    SHOW_SQL_ALCHEMY_QUERIES: int = 0

    DB_USER: str = "postgres"
    DB_PASS: str = "qwerty"
    DB_HOST: str = "127.0.0.1"
    DB_PORT: str = "5432"
    DB_NAME: str = "dbname"

    REDIS_USER: str = ""
    REDIS_PASSWORD: str = ""
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: str = "6379"

    POSTGRES_URL: Optional[str] = None
    REDIS_URL: Optional[str] = None

    WEBHOOK_HOST: str = "http://127.0.0.1"
    MAIN_BOT_TOKEN: str = "token"
    SECRET_TOKEN: str = "sectoken"
    ENABLE_LOCAL_BOTAPI: int = 0
    LOCAL_BOTAPI_URL: str = "http://localhost:8081"

    @field_validator("POSTGRES_URL")
    @classmethod
    def postgres_url(cls, v, values: FieldValidationInfo) -> str:
        db_user = values.data.get("DB_USER")
        db_pass = values.data.get("DB_PASS")
        db_host = values.data.get("DB_HOST")
        db_port = values.data.get("DB_PORT")
        db_name = values.data.get("DB_NAME")
        return f"postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    @field_validator("REDIS_URL")
    @classmethod
    def redis_url(cls, v, values: FieldValidationInfo) -> str:
        redis_user = values.data.get("REDIS_USER")
        redis_password = values.data.get("REDIS_PASSWORD")
        redis_host = values.data.get("REDIS_HOST")
        redis_port = values.data.get("REDIS_PORT")
        return f"redis://{redis_user}:{redis_password}@{redis_host}:{redis_port}"


secrets = Secrets()
