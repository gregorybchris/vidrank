from pydantic_settings import BaseSettings


class LoggingSettings(BaseSettings):
    """Logging settings."""

    log_level: str = "INFO"
