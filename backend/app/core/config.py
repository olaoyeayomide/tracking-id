from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    # App
    APP_NAME: str = "MCA Tracker"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]

    # Database
    DATABASE_URL: str

    # Security
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Carriers
    SENDBOX_API_KEY: str
    DHL_API_KEY: str | None = None
    GIG_API_KEY: str | None = None
    KWIK_API_KEY: str | None = None
    MAX_NG_API_KEY: str | None = None

    # Notifications
    TERMII_API_KEY: str | None = None
    SENDGRID_API_KEY: str | None = None
    WHATSAPP_BUSINESS_ID: str | None = None

    # Webhook
    WEBHOOK_SECRET: str = "webhook-secret-change-me"

    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 100
    SCRAPING_RATE_LIMIT: int = 5

    # Timeouts
    API_TIMEOUT: int = 30
    SCRAPING_TIMEOUT: int = 45

    # ✅ Modern way (no deprecation warnings)
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        extra="ignore",
        case_sensitive=True,
    )


settings = Settings()
