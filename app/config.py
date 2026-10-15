from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str = "sqlite:///./dev.db"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret: str = "development-only-change-me"
    access_token_minutes: int = 30
    ai_provider: str = "mock"
    ai_auto_accept_threshold: float = 0.95
    ai_human_review_threshold: float = 0.70
    portal_base_url: str = "http://localhost:9000"
    portal_username: str = "demo"
    portal_password: str = "demo-password"
    webhook_shared_secret: str = "development-webhook-secret"
    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_username: str | None = None
    smtp_password: str | None = None
    alert_email: str | None = None
    alert_webhook_url: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
