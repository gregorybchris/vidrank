from enum import StrEnum, auto


class MatchingStrategy(StrEnum):
    """Enum for different matching strategies."""

    BALANCED = auto()
    RANDOM = auto()
    BY_RATING = auto()
