from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    whatsapp_verify_token: str
    meta_app_secret: str
    whatsapp_access_token: str
    whatsapp_phone_number_id: str
    meta_graph_api_version: str = "v23.0"

    openai_api_key: str
    openai_model: str = "gpt-4o-mini"

    booking_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()