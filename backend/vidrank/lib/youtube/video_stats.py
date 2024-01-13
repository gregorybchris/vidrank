from typing import Any, Dict

from pydantic import BaseModel


class VideoStats(BaseModel):
    n_favorites: int
    n_comments: int
    n_dislikes: int
    n_likes: int
    n_views: int

    @classmethod
    def from_dict(cls, stats_dict: Dict[str, Any]) -> "VideoStats":
        stats_kwargs = {}
        stat_map = {
            "favoriteCount": "n_favorites",
            "commentCount": "n_comments",
            "dislikeCount": "n_dislikes",
            "likeCount": "n_likes",
            "viewCount": "n_views",
        }
        for youtube_stat, video_stat in stat_map.items():
            if youtube_stat not in stats_dict:
                stats_dict[youtube_stat] = 0
            stats_kwargs[video_stat] = stats_dict[youtube_stat]
        return cls(**stats_kwargs)
