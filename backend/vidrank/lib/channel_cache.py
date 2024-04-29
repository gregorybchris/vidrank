import logging
import pickle
from pathlib import Path
from typing import List, Optional

from vidrank.lib.youtube.channel import Channel

logger = logging.getLogger(__name__)


class ChannelCache:
    def __init__(self, cache_dirpath: Path):
        self.dirpath = cache_dirpath / "channels"
        self.ensure_exists()

    def ensure_exists(self) -> None:
        self.dirpath.mkdir(parents=True, exist_ok=True)

    def get(self, channel_id: str) -> Optional[Channel]:
        filepath = self.dirpath / f"{channel_id}.pkl"
        if not filepath.exists():
            return None

        with filepath.open("rb") as fp:
            return pickle.load(fp)

    def add(self, channel: Channel) -> None:
        self.ensure_exists()
        filepath = self.dirpath / f"{channel.id}.pkl"
        with filepath.open("wb") as fp:
            pickle.dump(channel, fp)

    def add_all(self, channels: List[Channel]) -> None:
        for channel in channels:
            self.add(channel)

    def has(self, channel_id: str) -> bool:
        filepath = self.dirpath / f"{channel_id}.pkl"
        return filepath.exists()
