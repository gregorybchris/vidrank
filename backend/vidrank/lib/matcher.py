import logging
from typing import ClassVar, List, Optional

import numpy as np

from vidrank.app.app_state import AppState
from vidrank.lib.action import Action
from vidrank.lib.matching_strategy import MatchingStrategy
from vidrank.lib.ranking.ranker import Ranker
from vidrank.lib.record import Record
from vidrank.lib.youtube.video import Video

logger = logging.getLogger(__name__)


class Matcher:
    DEFAULT_PROB_RANDOM: ClassVar[float] = 0.8

    @classmethod
    def match(
        cls,
        app_state: AppState,
        n_videos: int,
        matching_strategy: Optional[MatchingStrategy] = None,
        prob_random: float = DEFAULT_PROB_RANDOM,
    ) -> List[Video]:
        logger.info(f"Using matching strategy: {matching_strategy}")
        if matching_strategy == MatchingStrategy.RANDOM:
            return cls.match_random(app_state, n_videos)
        if matching_strategy == MatchingStrategy.BY_RATING:
            return cls.match_by_rating(app_state, n_videos)
        if matching_strategy in [None, MatchingStrategy.BALANCED]:
            r = app_state.rng.random()
            if r < prob_random:
                logger.info("Matching randomly")
                return cls.match_random(app_state, n_videos)
            logger.info("Matching by ratings")
            return cls.match_by_rating(app_state, n_videos)
        raise ValueError(f"Unknown matching strategy: {matching_strategy}")

    @classmethod
    def match_random(cls, app_state: AppState, n_videos: int) -> List[Video]:
        playlist = app_state.youtube_facade.get_playlist(app_state.playlist_id)

        records = app_state.record_tracker.load()
        non_removed_ids = cls.get_non_removed(playlist.video_ids, records)

        # Find videos that can be found in the YouTube API
        # NOTE: iter_videos can fail to find videos, so iterate until we have enough
        # or we run out of videos
        app_state.rng.shuffle(non_removed_ids)
        videos: List[Video] = []
        for video_id in non_removed_ids:
            if len(videos) == n_videos:
                return videos
            for video in app_state.youtube_facade.iter_videos([video_id]):
                videos.append(video)
                logger.info(f"Selected video: ({video.id}) {video.title}")

        return videos

    @classmethod
    def match_by_rating(cls, app_state: AppState, n_videos: int) -> List[Video]:
        records = app_state.record_tracker.load()

        # Rate all videos
        rankings = Ranker.rank(records)

        # If there are not enough ranked videos, return a random selection
        if len(rankings) < n_videos:
            logger.warning("Not enough ranked videos, will use random match")
            return cls.match_random(app_state, n_videos)

        # Select one video randomly
        selected_index: int = app_state.rng.choice(np.arange(len(rankings)))
        selected = rankings[selected_index]
        logger.info(f"Selecting videos similar to: rank={selected.rank}, rating={int(selected.rating)}")

        # Sort rankings based on distance to the selected video's rating
        sorted_rankings = sorted(rankings, key=lambda x: np.abs(selected.rating - x.rating))

        # Fetch video metadata for the most similar videos
        # NOTE: iter_videos can fail to find videos, so iterate until we have enough
        # or we run out of videos in the rankings
        videos: List[Video] = []
        for ranking in sorted_rankings:
            if len(videos) == n_videos:
                return videos
            for video in app_state.youtube_facade.iter_videos([ranking.video_id]):
                videos.append(video)
                logger.info(
                    f"Selected video: rank={ranking.rank}, rating={int(ranking.rating)}: ({video.id}) {video.title}"
                )

        return videos

    @classmethod
    def get_non_removed(cls, video_ids: List[str], records: List[Record]) -> List[str]:
        ids_set = set(video_ids)
        for record in records:
            ids_set -= set([c.video_id for c in record.choice_set.choices if c.action == Action.REMOVE])
        non_removed_ids = list(ids_set)
        return non_removed_ids
