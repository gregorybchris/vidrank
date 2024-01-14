from typing import List

from vidrank.app.app_state import AppState
from vidrank.lib.youtube.video import Video


def sample_videos(app_state: AppState, n_videos: int) -> List[Video]:
    playlist = app_state.youtube_facade.get_playlist(app_state.playlist_id)
    video_ids = app_state.rng.choice(playlist.video_ids, n_videos, replace=False)
    videos = list(app_state.youtube_facade.iter_videos(video_ids))
    return videos
