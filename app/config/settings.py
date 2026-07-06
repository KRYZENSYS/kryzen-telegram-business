from __future__ import annotations
from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore")
    bot_token: str = Field(default="", alias="BOT_TOKEN")
    super_admin_id: int = Field(default=0, alias="SUPER_ADMIN_ID")
    database_url: str = Field(default="sqlite+aiosqlite:///./kryzen.db", alias="DATABASE_URL")
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    jwt_secret: str = Field(default="dev-secret-must-be-long-enough-32b", alias="JWT_SECRET")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(default=60*24, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=30, alias="REFRESH_TOKEN_EXPIRE_DAYS")
    encryption_key: str = Field(default="", alias="ENCRYPTION_KEY")
    groq_api_key: str = Field(default="", alias="GROQ_API_KEY")
    groq_base_url: str = Field(default="https://api.groq.com/openai/v1", alias="GROQ_BASE_URL")
    groq_default_model: str = Field(default="llama-3.1-70b-versatile", alias="GROQ_DEFAULT_MODEL")
    ai_default_temperature: float = Field(default=0.7, alias="AI_DEFAULT_TEMPERATURE")
    ai_default_max_tokens: int = Field(default=1024, alias="AI_DEFAULT_MAX_TOKENS")
    cors_origins: str = Field(default="*", alias="CORS_ORIGINS")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    rate_limit_per_minute: int = Field(default=30, alias="RATE_LIMIT_PER_MINUTE")
    cleanup_days: int = Field(default=90, alias="CLEANUP_DAYS")
    app_host: str = Field(default="0.0.0.0", alias="APP_HOST")
    app_port: int = Field(default=8000, alias="APP_PORT")
    webhook_url: str = Field(default="", alias="WEBHOOK_URL")

@lru_cache
def get_settings() -> Settings: return Settings()
settings = get_settings()
