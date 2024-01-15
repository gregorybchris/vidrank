from pydantic import BaseModel


class Ranking(BaseModel):
    video_id: str
    rank: int
    score: float
