from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Finance Tracker"
    app_version: str = "0.1.0"
    api_prefix: str = "/api"
    database_url: str = "sqlite:///./finance_tracker.db"
    echo_sql: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
