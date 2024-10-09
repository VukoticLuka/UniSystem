from typing import Literal, List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from enum import Enum

PROJECT_PATH = Path(__file__).parent.parent.parent


class AppStage(Enum):
    DEVELOP = "develop"
    DEPLOY = "deploy"
    PRODUCTION = "production"


class Settings(BaseSettings):
    TEST_DB_URI: str = Field(default="sqlite+aiosqlite:///./test.db")
    DEV_STAGE: str = Field(default=AppStage.DEVELOP.value)
    DB_POOL_SIZE: int = Field(default=30)
    MAX_OVERFLOW: int = Field(default=10)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60)
    PROJECT_NAME: str = Field(default="MyFastApiProj")
    RUNNING_MODE: Literal["uvicorn"] | None = Field(default="uvicorn")
    BASE_URL: str = Field(default="http://localhost:8000")
    LISTENING_HOST: str = Field(default="0.0.0.0")  # noqa: S104
    LISTENING_PORT: int = Field(default=8000, gt=0, le=65535)
    CORS: List[str] = Field(default=["*"])

    model_config = SettingsConfigDict(env_file=f"{PROJECT_PATH}/.env", case_sensitive=True, extra="allow")


settings = Settings()
