import os
from pathlib import Path
from typing import TYPE_CHECKING, Optional

import numpy as np

from vidrank.lib.caching.pickle_cache import PickleCache
from vidrank.lib.caching.record_tracker import RecordTracker
from vidrank.lib.youtube.youtube_client import YouTubeClient
from vidrank.lib.youtube.youtube_facade import YouTubeFacade

if TYPE_CHECKING:
    from vidrank.lib.youtube.channel import Channel
    from vidrank.lib.youtube.playlist import Playlist
    from vidrank.lib.youtube.video import Video

from dataclasses import dataclass


@dataclass
class AppState:
    """AppState singleton."""

    _INSTANCE = None

    youtube_facade: YouTubeFacade
    record_tracker: RecordTracker
    playlist_id: str
    rng: np.random.Generator

    @classmethod
    def init(cls, random_seed: Optional[int] = None) -> "AppState":
        """Load the application state from environment variables.

        Args:
            random_seed (Optional[int]): The seed for random operations.

        Raises:
            ValueError: If any of the required environment variables are not set.
        """
        if cls._INSTANCE is not None:
            msg = "AppState has already been initialized"
            raise ValueError(msg)

        api_key = os.getenv("YOUTUBE_API_KEY")
        if api_key is None:
            msg = "YOUTUBE_API_KEY environment variable is not set."
            raise ValueError(msg)

        cache_dir_str = os.getenv("VIDRANK_CACHE_DIR")
        if cache_dir_str is None:
            msg = "VIDRANK_CACHE_DIR environment variable is not set."
            raise ValueError(msg)

        playlist_id = os.getenv("VIDRANK_PLAYLIST_ID")
        if playlist_id is None:
            msg = "VIDRANK_PLAYLIST_ID environment variable is not set."
            raise ValueError(msg)

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

        cls._INSTANCE = cls(
            youtube_facade=youtube_facade,
            record_tracker=record_tracker,
            playlist_id=playlist_id,
            rng=rng,
        )
        return cls._INSTANCE

    @classmethod
    def get(cls) -> "AppState":
        """Get the instance of the AppState singleton.

        Returns:
            AppState: The AppState instance.

        Raises:
            ValueError: If the AppState has not been initialized.
        """
        if cls._INSTANCE is None:
            return cls.init()

        return cls._INSTANCE
