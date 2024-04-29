from pydantic import BaseModel

from vidrank.lib.models.action import Action


class Choice(BaseModel):
    video_id: str
    action: Action
