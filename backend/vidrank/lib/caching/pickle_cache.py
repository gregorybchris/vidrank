import logging
import pickle
from pathlib import Path
from typing import Generic, Optional, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


class PickleCache(Generic[T]):
    def __init__(self, cache_dirpath: Path):
        self.dirpath = cache_dirpath

    def _ensure_exists(self) -> None:
        self.dirpath.mkdir(parents=True, exist_ok=True)

    def get(self, item_id: str) -> Optional[T]:
        filepath = self.dirpath / f"{item_id}.pkl"
        if not filepath.exists():
            return None

        with filepath.open("rb") as fp:
            return pickle.load(fp)

    def add(self, item_id: str, item: T) -> None:
        self._ensure_exists()
        filepath = self.dirpath / f"{item_id}.pkl"
        with filepath.open("wb") as fp:
            pickle.dump(item, fp)

    def has(self, item_id: str) -> bool:
        filepath = self.dirpath / f"{item_id}.pkl"
        return filepath.exists()

    def __len__(self) -> int:
        return len(list(self.dirpath.glob("*.pkl")))
