from dataclasses import dataclass

from vidrank.lib.transaction_tracker import TransactionTracker
from vidrank.lib.youtube_facade import YouTubeFacade


@dataclass
class AppState:
    _INSTANCE = None

    youtube_facade: YouTubeFacade
    transaction_tracker: TransactionTracker

    @classmethod
    def init(
        cls,
        *,
        youtube_facade: YouTubeFacade,
        transaction_tracker: TransactionTracker,
    ) -> None:
        cls._INSTANCE = cls(
            youtube_facade=youtube_facade,
            transaction_tracker=transaction_tracker,
        )

    @classmethod
    def get(cls) -> "AppState":
        if cls._INSTANCE is None:
            raise ValueError("AppState has not been initialized")

        return cls._INSTANCE
