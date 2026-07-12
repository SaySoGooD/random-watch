from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    TMDB_ACCESS_TOKEN: str
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    def get_object() -> Config:
        return Config()
