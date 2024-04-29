from typing import List

from pydantic import BaseModel

from vidrank.lib.youtube.playlist_item import PlaylistItem


class Playlist(BaseModel):
    id: str
    items: List[PlaylistItem]
