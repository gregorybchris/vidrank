import logging
import pickle
from pathlib import Path
from typing import List, Optional

from vidrank.lib.youtube.video import Video

logger = logging.getLogger(__name__)


class VideoCache:
    def __init__(self, cache_dirpath: Path):
        self.dirpath = cache_dirpath / "videos"
        self.ensure_exists()

    def ensure_exists(self) -> None:
        self.dirpath.mkdir(parents=True, exist_ok=True)

    def get(self, video_id: str) -> Optional[Video]:
        filepath = self.dirpath / f"{video_id}.pkl"
        if not filepath.exists():
            return None

        with filepath.open("rb") as fp:
            return pickle.load(fp)

    def add(self, video: Video) -> None:
        self.ensure_exists()
        filepath = self.dirpath / f"{video.id}.pkl"
        with filepath.open("wb") as fp:
            pickle.dump(video, fp)

    def add_all(self, videos: List[Video]) -> None:
        for video in videos:
            self.add(video)

    def has(self, video_id: str) -> bool:
        filepath = self.dirpath / f"{video_id}.pkl"
        return filepath.exists()
