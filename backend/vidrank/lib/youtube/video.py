from pydantic import BaseModel
from pydantic_extra_types.pendulum_dt import DateTime, Duration

from vidrank.lib.youtube.thumbnail_set import ThumbnailSet
from vidrank.lib.youtube.video_stats import VideoStats


class Video(BaseModel):
    """YouTube video model."""

    id: str
    title: str
    description: str
    duration: Duration
    channel_id: str
    channel: str
    published_at: DateTime
    thumbnails: ThumbnailSet
    stats: VideoStats
