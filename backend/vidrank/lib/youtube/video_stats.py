from pydantic import BaseModel


class VideoStats(BaseModel):
    """Video stats model."""

    n_favorites: int
    n_comments: int
    n_dislikes: int
    n_likes: int
    n_views: int
