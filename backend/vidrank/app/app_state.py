from dataclasses import dataclass

import numpy as np

from vidrank.lib.record_tracker import RecordTracker
from vidrank.lib.youtube_facade import YouTubeFacade


@dataclass
class AppState:
    _INSTANCE = None

    youtube_facade: YouTubeFacade
    record_tracker: RecordTracker
    playlist_id: str
    rng: np.random.Generator

    @classmethod
    def init(
        cls,
        *,
        youtube_facade: YouTubeFacade,
        record_tracker: RecordTracker,
        playlist_id: str,
        rng: np.random.Generator,
    ) -> None:
        cls._INSTANCE = cls(
            youtube_facade=youtube_facade,
            record_tracker=record_tracker,
            playlist_id=playlist_id,
            rng=rng,
        )

    @classmethod
    def get(cls) -> "AppState":
        if cls._INSTANCE is None:
            raise ValueError("AppState has not been initialized")

        return cls._INSTANCE
