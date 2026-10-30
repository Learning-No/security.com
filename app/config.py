from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Ironhaven API"
    environment: str = "development"
    secret_key: str = Field(min_length=32)
    database_url: str = "sqlite:///./ironhaven.db"
    access_token_minutes: int = Field(default=30, ge=5, le=1440)
    cors_origins: str = "http://localhost:3000,http://localhost:5173,http://127.0.0.1:5500"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
