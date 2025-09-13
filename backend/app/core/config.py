from pydantic_settings import BaseSettings
from pydantic import AnyUrl
from typing import Optional, List


class Settings(BaseSettings):
    APP_NAME: str = "AustraliaMortgageBrokerCRM"
    API_PREFIX: str = "/api"
    JWT_SECRET: str = "change-me"
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 14

    DB_URL: str = "postgresql+psycopg2://postgres:postgres@db:5432/postgres"
    REDIS_URL: str = "redis://redis:6379/0"

    CORS_ORIGINS: List[str] = ["http://localhost:5173"]

    AES_KEY_HEX: str = ""  # 64 hex chars for AES-256-GCM

    RATE_LIMIT: str = "100/minute"
    IP_BLACKLIST: List[str] = []

    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore

