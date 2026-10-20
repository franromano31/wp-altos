from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    whatsapp_verify_token: str
    meta_app_secret: str
    whatsapp_access_token: str
    whatsapp_phone_number_id: str
    meta_graph_api_version: str = "v23.0"

    database_url: str
    @field_validator("database_url")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        if value.startswith("postgresql://"):
            return value.replace(
                "postgresql://",
                "postgresql+asyncpg://",
                1,
            )
        return value

    postgres_password: str

    openai_api_key: str
    openai_model: str = "gpt-4o-mini"

    booking_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()