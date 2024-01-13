from typing import List

from pydantic import BaseModel


class Playlist(BaseModel):
    id: str
    name: str
    video_ids: List[str]
