from functools import lru_cache
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Entorno
    ENVIRONMENT: str = Field(default="development")
    DEBUG: bool = Field(default=False)
    LOG_LEVEL: str = Field(default="INFO")

    # API
    PROJECT_NAME: str = Field(default="Sistema de Asistencia Escolar")
    VERSION: str = Field(default="1.0.0")
    API_V1_PREFIX: str = Field(default="/api/v1")
    ALLOWED_HOSTS: List[str] = Field(default_factory=lambda: ["*"])

    # Seguridad
    SECRET_KEY: str = Field(default="insecure-secret-key-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60)

    # Base de datos
    DATABASE_URL: str = Field(default="sqlite:///./asistencia_escolar.db")


@lru_cache()
def get_settings() -> Settings:
    return Settings()