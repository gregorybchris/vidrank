import logging
import pickle
from pathlib import Path
from typing import List, Optional

from vidrank.lib.youtube.playlist import Playlist

logger = logging.getLogger(__name__)


class PlaylistCache:
    def __init__(self, cache_dirpath: Path):
        self.dirpath = cache_dirpath / "playlists"
        self.ensure_exists()

    def ensure_exists(self) -> None:
        self.dirpath.mkdir(parents=True, exist_ok=True)

    def get(self, playlist_id: str) -> Optional[Playlist]:
        filepath = self.dirpath / f"{playlist_id}.pkl"
        if not filepath.exists():
            return None

        with filepath.open("rb") as fp:
            return pickle.load(fp)

    def add(self, playlist: Playlist) -> None:
        self.ensure_exists()
        filepath = self.dirpath / f"{playlist.id}.pkl"
        with filepath.open("wb") as fp:
            pickle.dump(playlist, fp)

    def add_all(self, playlists: List[Playlist]) -> None:
        for playlist in playlists:
            self.add(playlist)

    def has(self, playlist_id: str) -> bool:
        filepath = self.dirpath / f"{playlist_id}.pkl"
        return filepath.exists()
