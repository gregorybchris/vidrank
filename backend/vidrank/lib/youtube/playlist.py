"""YouTube playlist model."""

from pydantic import BaseModel
from pydantic_extra_types.pendulum_dt import DateTime

from vidrank.lib.youtube.playlist_item import PlaylistItem
from vidrank.lib.youtube.thumbnail_set import ThumbnailSet


class Playlist(BaseModel):
    """YouTube playlist model."""

    id: str
    title: str
    created_at: DateTime
    thumbnails: ThumbnailSet
    description: str
    items: list[PlaylistItem]
