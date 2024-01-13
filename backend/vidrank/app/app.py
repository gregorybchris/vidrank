import contextlib
import logging
from dataclasses import dataclass
from typing import Iterator

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from vidrank.app.routes import router

logger = logging.getLogger(__name__)


@dataclass
class App:
    ALLOWED_ORIGINS = ["http://localhost:3000"]
    DEFAULT_HOST = "0.0.0.0"
    DEFAULT_PORT = 8000
    DEFAULT_LOG_LEVEL = logging.DEBUG

    fast_api: FastAPI
    host: str
    port: int
    log_level: int

    @classmethod
    @contextlib.contextmanager
    def context(
        cls,
        *,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
        log_level: int = DEFAULT_LOG_LEVEL,
    ) -> Iterator["App"]:
        fast_api = FastAPI()
        api = cls(fast_api=fast_api, host=host, port=port, log_level=log_level)

        fast_api.include_router(router)

        fast_api.add_middleware(
            CORSMiddleware,
            allow_origins=cls.ALLOWED_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        yield api

    def start(self) -> None:
        uvicorn.run(
            self.fast_api,
            host=self.host,
            port=self.port,
            log_level=self.log_level,
        )
