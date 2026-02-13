from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str = "sqlite:///./tickets.db"
    api_title: str = "Tickets API"
    api_version: str = "1.0.0"


settings = Settings()
