import logging
from typing import Iterator

import numpy as np

from vidrank.app.app_state import AppState
from vidrank.lib.models.action import Action
from vidrank.lib.models.matching_settings import MatchingSettings
from vidrank.lib.models.matching_strategy import MatchingStrategy
from vidrank.lib.models.record import Record
from vidrank.lib.ranking.ranker import Ranker
from vidrank.lib.youtube.video import Video

logger = logging.getLogger(__name__)


class Matcher:
    """Class to help determine which videos to return for comparison."""

    @classmethod
    def match(
        cls,
        app_state: AppState,
        n_videos: int,
        settings: MatchingSettings,
    ) -> Iterator[Video]:
        """Match videos based on the settings.

        Args:
            app_state (AppState): The application state.
            n_videos (int): The number of videos to return.
            settings (MatchingSettings): The matching settings.

        Yields:
            Iterator[Video]: An iterator over the matched videos

        Raises:
            ValueError: If the matching strategy is unknown.

        """
        logger.info("Using matching strategy: %s", settings.matching_strategy)
        if settings.matching_strategy == MatchingStrategy.RANDOM:
            yield from cls.match_random(app_state, n_videos)
        elif settings.matching_strategy == MatchingStrategy.BY_RATING:
            yield from cls.match_by_rating(app_state, n_videos)
        elif settings.matching_strategy in [None, MatchingStrategy.BALANCED]:
            logger.info("Using random fraction: %s", settings.balanced_random_fraction)
            r = app_state.rng.random()
            if r < settings.balanced_random_fraction:
                logger.info("Matching randomly")
                yield from cls.match_random(app_state, n_videos)
            else:
                logger.info("Matching by ratings")
                yield from cls.match_by_rating(app_state, n_videos)
        else:
            msg = f"Unknown matching strategy: {settings.matching_strategy}"
            raise ValueError(msg)

    @classmethod
    def match_random(cls, app_state: AppState, n_videos: int) -> Iterator[Video]:
        """Match videos using a random strategy.

        Args:
            app_state (AppState): The application state.
            n_videos (int): The number of videos to return.

        Yields:
            Iterator[Video]: An iterator over the matched videos

        """
        playlist = app_state.youtube_facade.get_playlist(app_state.playlist_id)

        records = app_state.record_tracker.load()
        playlist_video_ids = [item.video_id for item in playlist.items]
        non_removed_ids = cls.get_non_removed(playlist_video_ids, records)

        # Find videos that can be found in the YouTube API
        # NOTE: iter_videos can fail to find videos, so iterate until we have enough
        # or we run out of videos
        app_state.rng.shuffle(non_removed_ids)
        n_found = 0
        for video_id in non_removed_ids:
            if n_found == n_videos:
                return
            for video in app_state.youtube_facade.iter_videos([video_id]):
                logger.info("Selected video: (%s) %s", video.id, video.title)
                n_found += 1
                yield video

    @classmethod
    def match_by_rating(cls, app_state: AppState, n_videos: int) -> Iterator[Video]:
        """Match videos based on their ratings.

        Args:
            app_state (AppState): The application state.
            n_videos (int): The number of videos to return.

        Yields:
            Iterator[Video]: An iterator over the matched videos

        """
        playlist = app_state.youtube_facade.get_playlist(app_state.playlist_id)
        records = app_state.record_tracker.load()

        # Rate all videos
        rankings = list(Ranker.iter_rankings(records))

        # Filter for rankings for videos that are not removed
        playlist_video_ids = [item.video_id for item in playlist.items]
        non_removed_ids = cls.get_non_removed(playlist_video_ids, records)
        rankings = [r for r in rankings if r.video_id in non_removed_ids]

        # If there are not enough ranked videos, return a random selection
        if len(rankings) < n_videos:
            logger.warning("Not enough ranked videos, will use random match")
            yield from cls.match_random(app_state, n_videos)

        # Select one video randomly
        selected_index: int = app_state.rng.choice(np.arange(len(rankings)))
        selected = rankings[selected_index]
        logger.info("Selecting videos similar to: rank=%d, rating=%d", selected.rank, int(selected.rating))

        # Sort rankings based on distance to the selected video's rating
        sorted_rankings = sorted(rankings, key=lambda x: np.abs(selected.rating - x.rating))

        # Fetch video metadata for the most similar videos
        # NOTE: iter_videos can fail to find videos, so iterate until we have enough
        # or we run out of videos in the rankings
        n_found = 0
        for ranking in sorted_rankings:
            if n_found == n_videos:
                return
            for video in app_state.youtube_facade.iter_videos([ranking.video_id]):
                logger.info(
                    "Selected video: rank=%d, rating=%d: (%s) %s",
                    ranking.rank,
                    int(ranking.rating),
                    video.id,
                    video.title,
                )
                n_found += 1
                yield video

    @classmethod
    def get_non_removed(cls, video_ids: list[str], records: list[Record]) -> list[str]:
        """Return the video IDs that are not removed in the records.

        Args:
            video_ids (list[str]): The video IDs to check.
            records (list[Record]): The records to check against.

        Returns:
            list[str]: The video IDs that are not removed in the records.

        """
        ids_set = set(video_ids)
        for record in records:
            ids_set -= {c.video_id for c in record.choice_set.choices if c.action == Action.REMOVE}
        return list(ids_set)
