from dataclasses import dataclass

from vidrank.lib.playlist_cache import PlaylistCache
from vidrank.lib.transaction_tracker import TransactionTracker
from vidrank.lib.video_cache import VideoCache
from vidrank.lib.youtube.youtube_client import YouTubeClient
from vidrank.lib.youtube_facade import YouTubeFacade


@dataclass
class AppState:
    _INSTANCE = None

    youtube_client: YouTubeClient
    video_cache: VideoCache
    playlist_cache: PlaylistCache
    transaction_tracker: TransactionTracker
    youtube_facade: YouTubeFacade

    @classmethod
    def init(
        cls,
        *,
        youtube_client: YouTubeClient,
        video_cache: VideoCache,
        playlist_cache: PlaylistCache,
        transaction_tracker: TransactionTracker,
        youtube_facade: YouTubeFacade,
    ) -> None:
        cls._INSTANCE = cls(
            youtube_client=youtube_client,
            video_cache=video_cache,
            playlist_cache=playlist_cache,
            transaction_tracker=transaction_tracker,
            youtube_facade=youtube_facade,
        )

    @classmethod
    def get(cls) -> "AppState":
        if cls._INSTANCE is None:
            raise ValueError("AppState has not been initialized")

        return cls._INSTANCE
