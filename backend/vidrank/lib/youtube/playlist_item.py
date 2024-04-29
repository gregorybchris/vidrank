from pydantic import BaseModel
from pydantic_extra_types.pendulum_dt import DateTime


class PlaylistItem(BaseModel):
    video_id: str
    added_at: DateTime
