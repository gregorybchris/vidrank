from typing import List

from pydantic import BaseModel


class Playlist(BaseModel):
    id: str
    video_ids: List[str]
