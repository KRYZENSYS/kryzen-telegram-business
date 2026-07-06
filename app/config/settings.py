"""Centralized typed application settings.

Loads variables from .env and provides them as a typed Pydantic model.
Single source of truth for all configuration across the project.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # App
    app_name: str = "KRYZEN Telegram Business"
    app_env: Literal["development", "staging", "production"] = "production"
    app_debug: bool = False
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_timezone: str = "UTC"
    app_base_url: str = "http://localhost:8000"

    # Bot
    bot_token: str
    bot_webhook_secret: str = "kryzen_webhook"
    bot_webhook_url: str = ""
    bot_admin_chat_id: int = 0
    super_admin_id: int = 0

    # Database
    postgres_host: str = "postgres"
    postgres_port: int = 5432
    postgres_user: str = "kryzen"
    postgres_password: str
    postgres_db: str = "kryzen_business"
    database_url: str

    # Redis
    redis_host: str = "redis"
    redis_port: int = 6379
    redis_password: str = ""
    redis_db: int = 0
    redis_url: str

    # Security
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_access_ttl: int = 3600
    jwt_refresh_ttl: int = 2_592_000
    encryption_key: str

    # Groq
    groq_api_key: str
    groq_base_url: str = "https://api.groq.com/openai/v1"
    groq_default_model: str = "llama-3.3-70b-versatile"
    groq_fallback_model: str = "llama-3.1-8b-instant"
    groq_timeout: int = 30
    groq_max_retries: int = 2

    # Business
    business_api_enabled: bool = True
    business_bot_username: str = "YourBusinessBot"

    # Premium
    premium_default_days: int = 30
    premium_trial_days: int = 7
    free_archive_days: int = 7
    premium_archive_days: int = 0  # 0 = unlimited

    # Rate limit
    rate_limit_per_minute: int = 60
    rate_limit_per_day: int = 10_000
    broadcast_rate: int = 25

    # Logging
    log_level: str = "INFO"
    log_file: str = "/app/logs/app.log"
    log_max_bytes: int = 10_485_760
    log_backup_count: int = 10

    # Webhook / Mini App
    mini_app_url: str = "https://your-domain.com/miniapp"
    webhook_host: str = "0.0.0.0"
    webhook_port: int = 8080

    # Backup
    backup_enabled: bool = True
    backup_path: str = "/app/backups"
    backup_retention_days: int = 14

    @field_validator("database_url")
    @classmethod
    def _validate_db_url(cls, v: str) -> str:
        if not v.startswith(("postgresql+asyncpg://", "sqlite+aiosqlite://")):
            raise ValueError("DATABASE_URL must use asyncpg or aiosqlite driver")
        return v

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    @property
    def project_root(self) -> Path:
        return Path(__file__).resolve().parent.parent.parent

    @property
    def log_dir(self) -> Path:
        p = Path(self.log_file).parent
        p.mkdir(parents=True, exist_ok=True)
        return p


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Cached settings accessor (DI friendly)."""
    return Settings()  # type: ignore[call-arg]


settings: Settings = get_settings()
