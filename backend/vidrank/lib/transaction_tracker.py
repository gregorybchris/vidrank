import json
from pathlib import Path
from typing import List

from vidrank.lib.transaction import Transaction


class TransactionTracker:
    def __init__(self, cache_dirpath: Path):
        self.dirpath = cache_dirpath / "transactions"
        self.dirpath.mkdir(parents=True, exist_ok=True)
        self.filepath = self.dirpath / "transactions.json"

    def load(self) -> List[Transaction]:
        if not self.filepath.exists():
            return []
        with self.filepath.open("r") as fp:
            transactions_json = json.load(fp)
            return [Transaction(**t) for t in transactions_json]

    def add(self, transaction: Transaction) -> None:
        transactions = self.load()
        transactions.append(transaction)
        transactions_json = [t.model_dump() for t in transactions]
        with self.filepath.open("w") as fp:
            json.dump(transactions_json, fp)
