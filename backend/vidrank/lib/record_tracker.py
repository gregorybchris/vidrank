import json
from pathlib import Path
from typing import List, Optional

from vidrank.lib.record import Record


class RecordTracker:
    def __init__(self, cache_dirpath: Path):
        self.dirpath = cache_dirpath / "records"
        self.filepath = self.dirpath / "records.json"
        self.ensure_exists()

    def ensure_exists(self) -> None:
        self.dirpath.mkdir(parents=True, exist_ok=True)

    def load(self) -> List[Record]:
        if not self.filepath.exists():
            return []
        with self.filepath.open("r") as fp:
            records_json = json.load(fp)
            return [Record(**t) for t in records_json]

    def add(self, record: Record) -> None:
        self.ensure_exists()
        records = self.load()
        records.append(record)
        records_json = [t.model_dump() for t in records]
        with self.filepath.open("w") as fp:
            json.dump(records_json, fp)

    def pop(self, record_id: str) -> Optional[Record]:
        self.ensure_exists()
        records = self.load()
        new_records = [r for r in records if r.id != record_id]
        for record in records:
            if record.id == record_id:
                records_json = [t.model_dump() for t in new_records]
                with self.filepath.open("w") as fp:
                    json.dump(records_json, fp)
                return record
        return None
