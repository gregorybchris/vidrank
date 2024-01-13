import logging
import pickle
from pathlib import Path
from typing import List, Optional

from vidrank.lib.youtube.video import Video

logger = logging.getLogger(__name__)


class VideoCache:
    def __init__(self, cache_dirpath: Path):
        self.cache_dirpath = cache_dirpath

    def get(self, video_id: str) -> Optional[Video]:
        video_filepath = self.cache_dirpath / f"{video_id}.pkl"
        if not video_filepath.exists():
            return None

        with video_filepath.open("rb") as fp:
            video = pickle.load(fp)
            return video

    def add(self, video: Video) -> None:
        video_filepath = self.cache_dirpath / f"{video.id}.pkl"
        with video_filepath.open("wb") as fp:
            pickle.dump(video, fp)

    def add_all(self, videos: List[Video]) -> None:
        for video in videos:
            self.add(video)

    def has(self, video_id: str) -> bool:
        video_filepath = self.cache_dirpath / f"{video_id}.pkl"
        return video_filepath.exists()
