from pydantic import BaseModel


class ChannelStats(BaseModel):
    """YouTube channel stats model."""

    subscribers: int
    videos: int
    views: int
