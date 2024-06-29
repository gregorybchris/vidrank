import logging
import pickle
from pathlib import Path
from typing import Generic, Optional, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


class PickleCache(Generic[T]):
    """Cache that stores items on disk using pickle."""

    def __init__(self, cache_dirpath: Path):
        """Initialize the pickle cache.

        Args:
            cache_dirpath (Path): The path to the cache directory.

        """
        self.dirpath = cache_dirpath

    def _ensure_exists(self) -> None:
        self.dirpath.mkdir(parents=True, exist_ok=True)

    def get(self, item_id: str) -> Optional[T]:
        """Get an item from the cache.

        Args:
            item_id (str): The ID of the item to fetch.

        Returns:
            Optional[T]: The item with the given ID, or None if it does not exist.

        """
        filepath = self.dirpath / f"{item_id}.pkl"
        if not filepath.exists():
            return None

        with filepath.open("rb") as fp:
            return pickle.load(fp)

    def add(self, item_id: str, item: T) -> None:
        """Add an item to the cache.

        Args:
            item_id (str): The ID of the item to add.
            item (T): The item to add to the cache.

        """
        self._ensure_exists()
        filepath = self.dirpath / f"{item_id}.pkl"
        with filepath.open("wb") as fp:
            pickle.dump(item, fp)

    def has(self, item_id: str) -> bool:
        """Check if an item is in the cache.

        Args:
            item_id (str): The ID of the item to check.

        Returns:
            bool: True if the item is in the cache, False otherwise.

        """
        filepath = self.dirpath / f"{item_id}.pkl"
        return filepath.exists()

    def __len__(self) -> int:
        """Get the number of items in the cache.

        Returns:
            int: The number of items in the cache.

        """
        return len(list(self.dirpath.glob("*.pkl")))
