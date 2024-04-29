from enum import StrEnum, auto


class MatchingStrategy(StrEnum):
    BALANCED = auto()
    RANDOM = auto()
    BY_RATING = auto()
