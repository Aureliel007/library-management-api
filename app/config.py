from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PG_DSN: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/test-base"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    
    model_config = SettingsConfigDict(env_file=".env")

settings: Settings = Settings()