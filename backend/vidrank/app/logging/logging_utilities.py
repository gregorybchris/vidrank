from logging.config import dictConfig

from vidrank.app.logging.logging_config import LoggingConfig
from vidrank.app.logging.logging_settings import LoggingSettings


def configure_logger() -> None:
    """Configure the logger with the log level from the environment."""
    settings = LoggingSettings()
    config = LoggingConfig(log_level=settings.log_level)
    dictConfig(config.model_dump())
