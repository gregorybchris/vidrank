from enum import StrEnum, auto


class Action(StrEnum):
    SELECT = auto()
    NOTHING = auto()
    REMOVE = auto()
