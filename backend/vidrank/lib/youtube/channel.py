from pydantic import BaseModel

from vidrank.lib.youtube.channel_stats import ChannelStats
from vidrank.lib.youtube.thumbnail_set import ThumbnailSet


class Channel(BaseModel):
    id: str
    name: str
    url: str
    thumbnails: ThumbnailSet
    stats: ChannelStats
