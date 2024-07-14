from pydantic import BaseModel
from pydantic_extra_types.pendulum_dt import DateTime

from vidrank.lib.youtube.thumbnail_set import ThumbnailSet


class PlaylistItem(BaseModel):
    """Playlist item model."""

    video_id: str
    added_at: DateTime
    position: int
    title: str
    description: str
    thumbnails: ThumbnailSet
