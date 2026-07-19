from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    TMDB_ACCESS_TOKEN: str

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_TITLE: str = "Random Watch API"
    API_VERSION: str = "0.1.0"
    API_RATE_LIMIT_PER_CLIENT: int = 35
    API_RATE_LIMIT_GLOBAL: int = 35
    API_RATE_LIMIT_WINDOW: int = 10

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )