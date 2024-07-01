from pydantic import BaseModel, computed_field


class LoggingConfig(BaseModel):
    """Logging configuration for the application."""

    version: int = 1
    log_level: str = "INFO"
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s | %(asctime)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }

    @computed_field
    def loggers(self) -> dict:
        """Loggers configuration."""
        return {
            "vidrank": {
                "handlers": ["default"],
                "level": self.log_level,
            },
        }
