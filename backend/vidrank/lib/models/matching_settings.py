from typing import Optional

from pydantic import BaseModel


class ByDateStrategySettings(BaseModel):
    """By date strategy settings model."""

    days: int


class ByRatingStrategySettings(BaseModel):
    """By rating strategy settings model."""


class FinetuneStrategySettings(BaseModel):
    """Finetune strategy settings model."""

    fraction: float


class RandomStrategySettings(BaseModel):
    """Random strategy settings model."""


class MatchingSettings(BaseModel):
    """Matching settings model."""

    by_date_strategy: Optional[ByDateStrategySettings]
    by_rating_strategy: Optional[ByRatingStrategySettings]
    finetune_strategy: Optional[FinetuneStrategySettings]
    random_strategy: Optional[RandomStrategySettings]
