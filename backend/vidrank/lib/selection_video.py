from pydantic import BaseModel

from vidrank.lib.action import Action


class SelectionVideo(BaseModel):
    video_id: str
    action: Action
