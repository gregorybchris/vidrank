from typing import Optional

from pydantic import BaseModel
from pydantic_extra_types.pendulum_dt import DateTime, Duration

from vidrank.lib.youtube.thumbnail_set import ThumbnailSet
from vidrank.lib.youtube.video_stats import VideoStats


# pylint: disable=redefined-builtin
class Video(BaseModel):
    id: str
    title: str
    duration: Duration
    channel_id: Optional[str] = None
    channel: str
    publish_datetime: DateTime
    thumbnails: ThumbnailSet
    stats: VideoStats
