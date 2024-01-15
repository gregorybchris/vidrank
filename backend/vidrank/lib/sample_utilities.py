from typing import List

import numpy as np

from vidrank.app.app_state import AppState
from vidrank.lib.action import Action
from vidrank.lib.ranking.ranker import Ranker
from vidrank.lib.youtube.video import Video


def sample_videos_by_rating(app_state: AppState, n_videos: int) -> List[Video]:
    playlist = app_state.youtube_facade.get_playlist(app_state.playlist_id)

    # Find video IDs that have not been tagged for removal
    ids_set = set(playlist.video_ids)
    records = app_state.record_tracker.load()
    for record in records:
        ids_set -= set([c.video_id for c in record.choice_set.choices if c.action == Action.REMOVE])
    acceptable_ids = list(ids_set)

    # If there are not enough videos to sample from, return all of them
    if len(acceptable_ids) < n_videos:
        return list(app_state.youtube_facade.iter_videos(acceptable_ids))

    # Rate all videos
    rankings = Ranker.rank(records)

    # Select one video randomly
    selected_index: int = app_state.rng.choice(np.arange(len(rankings)))
    selected = rankings[selected_index]
    print("Selecting videos similar to: ", selected.rank)

    # Sort rankings based on distance to the selected video's rating
    sorted_rankings = sorted(rankings, key=lambda x: np.abs(selected.rating - x.rating))

    # Fetch video metadata for the most similar videos
    videos: List[Video] = []
    for ranking in sorted_rankings:
        if len(videos) == n_videos:
            return videos
        for video in app_state.youtube_facade.iter_videos([ranking.video_id]):
            videos.append(video)

            print("======")
            print("title: ", video.title)
            print("id: ", video.id)
            print("rating: ", ranking.rating)
            print("rank: ", ranking.rank)
    return videos
