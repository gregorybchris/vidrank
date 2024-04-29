import contextlib
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Optional

import numpy as np
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from vidrank.app.app_state import AppState
from vidrank.app.routes import router
from vidrank.lib.pickle_cache import PickleCache
from vidrank.lib.record_tracker import RecordTracker
from vidrank.lib.youtube.channel import Channel
from vidrank.lib.youtube.playlist import Playlist
from vidrank.lib.youtube.video import Video
from vidrank.lib.youtube.youtube_client import YouTubeClient
from vidrank.lib.youtube_facade import YouTubeFacade

logger = logging.getLogger(__name__)


@dataclass
class App:
    ALLOWED_ORIGINS = ["http://localhost:3000"]
    DEFAULT_HOST = "0.0.0.0"
    DEFAULT_PORT = 8000
    DEFAULT_LOG_LEVEL = logging.INFO
    DEFAULT_RANDOM_SEED = None

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
        random_seed: Optional[int] = DEFAULT_RANDOM_SEED
    ) -> Iterator["App"]:
        fast_api = FastAPI()
        api = cls(fast_api=fast_api, host=host, port=port, log_level=log_level)

        cls.load_app_state(random_seed=random_seed)

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
    def load_app_state(cls, random_seed: Optional[int] = DEFAULT_RANDOM_SEED) -> None:
        api_key = os.getenv("YOUTUBE_API_KEY")
        if api_key is None:
            raise ValueError("YOUTUBE_API_KEY environment variable is not set.")

        cache_dir_str = os.getenv("VIDRANK_CACHE_DIR")
        if cache_dir_str is None:
            raise ValueError("VIDRANK_CACHE_DIR environment variable is not set.")

        playlist_id = os.getenv("VIDRANK_PLAYLIST_ID")
        if playlist_id is None:
            raise ValueError("VIDRANK_PLAYLIST_ID environment variable is not set.")

        cache_dirpath = Path(cache_dir_str)
        youtube_client = YouTubeClient(api_key)
        video_cache: PickleCache[Video] = PickleCache(cache_dirpath / "videos")
        channel_cache: PickleCache[Channel] = PickleCache(cache_dirpath / "channels")
        playlist_cache: PickleCache[Playlist] = PickleCache(cache_dirpath / "playlists")
        youtube_facade = YouTubeFacade(
            youtube_client=youtube_client,
            video_cache=video_cache,
            channel_cache=channel_cache,
            playlist_cache=playlist_cache,
        )
        record_tracker = RecordTracker(cache_dirpath)
        rng = np.random.default_rng(random_seed)

        AppState.init(
            youtube_facade=youtube_facade,
            record_tracker=record_tracker,
            playlist_id=playlist_id,
            rng=rng,
        )

    def start(self) -> None:
        uvicorn.run(
            self.fast_api,
            host=self.host,
            port=self.port,
            log_level=self.log_level,
        )
