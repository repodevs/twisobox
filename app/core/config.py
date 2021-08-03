import secrets
from typing import List, Optional, Union

from pydantic import BaseSettings
from pydantic.class_validators import validator
from pydantic.networks import AnyHttpUrl, PostgresDsn


class Settings(BaseSettings):
    PROJECT_NAME: str = "TwisoBox"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRES_IN_MINUTES: int = 60 * 24 * 8
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    class Config:
        case_sensitive = True
        # dotenv
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
