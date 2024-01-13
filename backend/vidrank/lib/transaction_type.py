from enum import StrEnum, auto


class TransactionType(StrEnum):
    UNDO = auto()
    SKIP = auto()
    SUBMIT = auto()
