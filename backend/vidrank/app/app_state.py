"""AppState singleton."""

from dataclasses import dataclass

import numpy as np

from vidrank.lib.caching.record_tracker import RecordTracker
from vidrank.lib.youtube.youtube_facade import YouTubeFacade


@dataclass
class AppState:
    """AppState singleton."""

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
        """Initialize the AppState singleton.

        Args:
            youtube_facade (YouTubeFacade): The YouTubeFacade instance.
            record_tracker (RecordTracker): The RecordTracker instance.
            playlist_id (str): The ID of the playlist.
            rng (np.random.Generator): The random number generator.

        """
        cls._INSTANCE = cls(
            youtube_facade=youtube_facade,
            record_tracker=record_tracker,
            playlist_id=playlist_id,
            rng=rng,
        )

    @classmethod
    def get(cls) -> "AppState":
        """Get the instance of the AppState singleton.

        Returns:
            AppState: The AppState instance.

        Raises:
            ValueError: If the AppState has not been initialized.
        """
        if cls._INSTANCE is None:
            msg = "AppState has not been initialized"
            raise ValueError(msg)

        return cls._INSTANCE
