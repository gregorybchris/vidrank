from pydantic import BaseModel

from vidrank.lib.models.matching_strategy import MatchingStrategy


class MatchingSettings(BaseModel):
    matching_strategy: MatchingStrategy
    balanced_random_fraction: float
