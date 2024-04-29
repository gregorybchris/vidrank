from pydantic import BaseModel


class ChannelStats(BaseModel):
    subscribers: int
    videos: int
    views: int
