from typing import Any, Dict, List, cast

import pendulum
from pendulum import DateTime, Duration
from pydantic import BaseModel

from vidrank.lib.youtube.thumbnail_set import ThumbnailSet
from vidrank.lib.youtube.video_stats import VideoStats


# pylint: disable=redefined-builtin
class Video(BaseModel):
    id: str
    title: str
    duration: Duration
    channel: str
    publish_datetime: DateTime
    tags: List[str]
    thumbnails: ThumbnailSet
    stats: VideoStats

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_dict(cls, video_dict: Dict[str, Any]) -> "Video":
        duration = pendulum.parse(video_dict["contentDetails"]["duration"])
        publish_datetime = pendulum.parse(video_dict["snippet"]["publishedAt"])
        return Video(
            id=video_dict["id"],
            title=video_dict["snippet"]["title"],
            duration=cast(Duration, duration),
            channel=video_dict["snippet"]["channelTitle"],
            publish_datetime=cast(DateTime, publish_datetime),
            tags=video_dict["snippet"]["tags"],
            thumbnails=ThumbnailSet.from_dict(video_dict["snippet"]["thumbnails"]),
            stats=VideoStats.from_dict(video_dict["statistics"]),
        )

    def serialize(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "duration": self.duration.in_seconds(),
            "channel": self.channel,
            "publish_datetime": self.publish_datetime.to_iso8601_string(),
            "tags": self.tags,
            "thumbnails": self.thumbnails.model_dump(),
            "stats": self.stats.model_dump(),
        }
