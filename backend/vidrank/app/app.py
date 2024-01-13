import contextlib
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from vidrank.app.app_state import AppState
from vidrank.app.routes import router
from vidrank.lib.playlist_cache import PlaylistCache
from vidrank.lib.transaction_tracker import TransactionTracker
from vidrank.lib.video_cache import VideoCache
from vidrank.lib.youtube.youtube_client import YouTubeClient
from vidrank.lib.youtube_facade import YouTubeFacade

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

        cls.load_app_state()

        fast_api.include_router(router)

        fast_api.add_middleware(
            CORSMiddleware,
            allow_origins=cls.ALLOWED_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        yield api

    @classmethod
    def load_app_state(cls) -> None:
        api_key = os.getenv("YOUTUBE_API_KEY")
        if api_key is None:
            raise ValueError("YOUTUBE_API_KEY environment variable is not set.")

        cache_dir_str = os.getenv("VIDRANK_CACHE_DIR")
        if cache_dir_str is None:
            raise ValueError("VIDRANK_CACHE_DIR environment variable is not set.")

        cache_dirpath = Path(cache_dir_str)
        youtube_client = YouTubeClient(api_key)
        video_cache = VideoCache(cache_dirpath)
        playlist_cache = PlaylistCache(cache_dirpath)
        transaction_tracker = TransactionTracker(cache_dirpath)
        youtube_facade = YouTubeFacade(
            youtube_client=youtube_client,
            video_cache=video_cache,
            playlist_cache=playlist_cache,
        )

        AppState.init(
            youtube_client=youtube_client,
            video_cache=video_cache,
            playlist_cache=playlist_cache,
            transaction_tracker=transaction_tracker,
            youtube_facade=youtube_facade,
        )

    def start(self) -> None:
        uvicorn.run(
            self.fast_api,
            host=self.host,
            port=self.port,
            log_level=self.log_level,
        )
