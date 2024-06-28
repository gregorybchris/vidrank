"""Ranking model."""

from pydantic import BaseModel


class Ranking(BaseModel):
    """Ranking model."""

    video_id: str
    rank: int
    rating: float
