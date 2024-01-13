from pydantic import BaseModel


class SelectionVideo(BaseModel):
    video_id: str
    selected: bool
