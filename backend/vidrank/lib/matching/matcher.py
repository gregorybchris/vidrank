import logging
from typing import TYPE_CHECKING, Iterator

import numpy as np
import pendulum

from vidrank.app.app_state import AppState
from vidrank.lib.models.action import Action
from vidrank.lib.models.matching_settings import ByDateStrategySettings, FinetuneStrategySettings, MatchingSettings
from vidrank.lib.models.record import Record
from vidrank.lib.ranking.ranker import Ranker
from vidrank.lib.youtube.video import Video

if TYPE_CHECKING:
    from vidrank.lib.ranking.ranking import Ranking
    from vidrank.lib.youtube.playlist_item import PlaylistItem

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
        if settings.by_date_strategy is not None:
            logger.info("Using matching strategy: by_date")
            yield from cls.match_by_date(app_state, n_videos, settings.by_date_strategy)
        elif settings.by_rating_strategy is not None:
            logger.info("Using matching strategy: by_rating")
            yield from cls.match_by_rating(app_state, n_videos)
        elif settings.finetune_strategy is not None:
            logger.info("Using matching strategy: finetune")
            yield from cls.match_finetune(app_state, n_videos, settings.finetune_strategy)
        elif settings.random_strategy is not None:
            logger.info("Using matching strategy: random")
            yield from cls.match_random(app_state, n_videos)
        else:
            logger.info("No matching strategy specified, using default: random")
            yield from cls.match_random(app_state, n_videos)

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
            Iterator[Video]: An iterator over the matched videos.
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
    def match_finetune(cls, app_state: AppState, n_videos: int, settings: FinetuneStrategySettings) -> Iterator[Video]:
        """Match videos from the upper part of rankings.

        Args:
            app_state (AppState): The application state.
            n_videos (int): The number of videos to return.
            settings (FinetuneStrategySettings): The finetune strategy settings.

        Yields:
            Iterator[Video]: An iterator over the matched videos.
        """
        playlist = app_state.youtube_facade.get_playlist(app_state.playlist_id)
        records = app_state.record_tracker.load()

        # Rate all videos
        rankings = list(Ranker.iter_rankings(records))

        # Filter for rankings for videos that are not removed
        playlist_video_ids = [item.video_id for item in playlist.items]
        non_removed_ids = cls.get_non_removed(playlist_video_ids, records)
        rankings = [r for r in rankings if r.video_id in non_removed_ids]

        n_top_rankings = int(len(rankings) * settings.fraction)

        # If there are not enough ranked videos, return a random selection
        if n_top_rankings < n_videos:
            logger.warning("Not enough ranked videos, will use random match")
            yield from cls.match_random(app_state, n_videos)

        # Randomly sample from the top half of videos
        selected_indices: np.ndarray = app_state.rng.choice(n_top_rankings, n_top_rankings, replace=False)
        top_rankings: list[Ranking] = [rankings[i] for i in selected_indices]

        # Fetch video metadata for the most similar videos
        # NOTE: iter_videos can fail to find videos, so iterate until we have enough
        # or we run out of videos in the rankings
        n_found = 0
        for ranking in top_rankings:
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
    def match_by_date(cls, app_state: AppState, n_videos: int, settings: ByDateStrategySettings) -> Iterator[Video]:
        """Match videos added to the playlist most recently.

        Args:
            app_state (AppState): The application state.
            n_videos (int): The number of videos to return.
            settings (ByDateStrategySettings): The by date strategy settings.

        Yields:
            Iterator[Video]: An iterator over the matched videos.
        """
        playlist = app_state.youtube_facade.get_playlist(app_state.playlist_id)
        items = playlist.items

        # Sort items by date added
        sorted_items = sorted(items, key=lambda x: x.added_at, reverse=True)

        # Filter for items within the date range
        n_days = settings.days
        now = pendulum.now()
        filtered_items = [item for item in sorted_items if (now - item.added_at).days <= n_days]
        n_within_range = len(filtered_items)

        # If there are not enough videos within the date range, return a random selection
        if n_within_range < n_videos:
            logger.warning("Not enough videos within the date range, will use random match")
            yield from cls.match_random(app_state, n_videos)

        # Randomly sample from the most recently added videos
        selected_indices: np.ndarray = app_state.rng.choice(n_within_range, n_within_range, replace=False)
        latest_items: list[PlaylistItem] = [filtered_items[i] for i in selected_indices]

        # Fetch video metadata for the most recently added videos
        # NOTE: iter_videos can fail to find videos, so iterate until we have enough
        # or we run out of videos in the rankings
        n_found = 0
        for item in latest_items:
            if n_found == n_videos:
                return
            for video in app_state.youtube_facade.iter_videos([item.video_id]):
                logger.info("Selected video: (%s) %s", video.id, video.title)
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
