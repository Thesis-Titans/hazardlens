from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_user: str = "hazardlens"
    postgres_password: str = "changeme"
    postgres_db: str = "hazardlens"
    database_url: str = "postgresql+asyncpg://hazardlens:changeme@db:5432/hazardlens"
    secret_key: str = "changeme"
    gemini_api_key: str = ""
    openrouter_api_key: str = ""
    ollama_base_url: str = "http://host.docker.internal:11434"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
