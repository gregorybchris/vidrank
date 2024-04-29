from pydantic import BaseModel


class VideoStats(BaseModel):
    n_favorites: int
    n_comments: int
    n_dislikes: int
    n_likes: int
    n_views: int
