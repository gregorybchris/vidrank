from typing import List

from vidrank.app.app_state import AppState
from vidrank.lib.action import Action
from vidrank.lib.youtube.video import Video


def sample_videos(app_state: AppState, n_videos: int) -> List[Video]:
    playlist = app_state.youtube_facade.get_playlist(app_state.playlist_id)

    # Find video IDs that have not been tagged for removal
    ids_set = set(playlist.video_ids)
    records = app_state.record_tracker.load()
    for record in records:
        ids_set -= set([c.video_id for c in record.choice_set.choices if c.action == Action.REMOVE])
    acceptable_ids = list(ids_set)

    # Find videos that can be found in the YouTube API
    videos: List[Video] = []
    while len(videos) < n_videos:
        sample_ids = app_state.rng.choice(acceptable_ids, n_videos - len(videos), replace=False)
        new_videos = app_state.youtube_facade.iter_videos(sample_ids)
        for video in new_videos:
            if video not in videos:
                videos.append(video)

    return videos
