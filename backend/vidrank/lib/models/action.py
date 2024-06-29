from enum import StrEnum, auto


class Action(StrEnum):
    """Enum for different actions."""

    SELECT = auto()
    NOTHING = auto()
    REMOVE = auto()
