"""Local cache for saving records on disk."""

import json
from pathlib import Path
from typing import Optional

from vidrank.lib.models.record import Record


class RecordTracker:
    """Local cache for saving records on disk."""

    def __init__(self, cache_dirpath: Path):
        """Initialize the record tracker.

        Args:
        ----
        cache_dirpath (Path): The path to the cache directory.

        """
        self.dirpath = cache_dirpath / "records"
        self.filepath = self.dirpath / "records.json"
        self.ensure_exists()

    def ensure_exists(self) -> None:
        """Ensure that the cache directory exists."""
        self.dirpath.mkdir(parents=True, exist_ok=True)

    def load(self) -> list[Record]:
        """Load the records from the cache.

        Returns
        -------
        list[Record]: The records loaded from the cache.

        """
        if not self.filepath.exists():
            return []
        with self.filepath.open("r") as fp:
            records_json = json.load(fp)
            return [Record(**r) for r in records_json]

    def add(self, record: Record) -> None:
        """Add a record to the cache.

        Args:
        ----
        record (Record): The record to add to the cache.

        """
        self.ensure_exists()
        records = self.load()
        records.append(record)
        records_json = [r.model_dump() for r in records]
        with self.filepath.open("w") as fp:
            json.dump(records_json, fp)

    def pop(self, record_id: str) -> Optional[Record]:
        """Pop a record from the cache.

        Args:
        ----
        record_id (str): The ID of the record to pop from the cache.

        Returns:
        -------
        Optional[Record]: The record popped from the cache, or None if not found.

        """
        self.ensure_exists()
        records = self.load()
        for record in records:
            if record.id == record_id:
                records_json = [r.model_dump() for r in records if r.id != record_id]
                with self.filepath.open("w") as fp:
                    json.dump(records_json, fp)
                return record
        return None
