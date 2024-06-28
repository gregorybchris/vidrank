"""Command-line interface for the VidRank application."""

import logging
from itertools import islice
from typing import Any

import click

from vidrank.app.app import App
from vidrank.app.app_state import AppState
from vidrank.lib.analytics.analytics import print_ratings_histogram
from vidrank.lib.models.action import Action
from vidrank.lib.ranking.ranker import Ranker
from vidrank.lib.utilities.io_utilities import print_channel, print_playlist, print_video
from vidrank.lib.utilities.url_utilities import url_from_video_id

logger = logging.getLogger(__name__)

# ruff: noqa: T201


@click.group()
def main() -> None:
    """Run main CLI entrypoint."""


@main.command()
@click.option("--host", "host", type=str, default=App.DEFAULT_HOST)
@click.option("--port", "port", type=int, default=App.DEFAULT_PORT)
@click.option("--debug", type=bool, default=False, is_flag=True)
def serve(debug: bool = False, **kwargs: Any) -> None:
    """Start the server.

    Args:
        debug (bool): Whether to enable debug logging.
        kwargs (Any): Additional keyword arguments.

    """
    if debug:
        logging.basicConfig(level=logging.INFO)

    with App.context(**kwargs) as app:
        app.start()


@main.command(name="video")
@click.argument("video_id", type=str)
@click.option("--use-cache/--no-cache", default=True)
@click.option("--debug", type=bool, default=False, is_flag=True)
def get_video(
    video_id: str,
    use_cache: bool,
    debug: bool = False,
) -> None:
    """Get video information.

    Args:
        video_id (str): The ID of the video to get information for.
        use_cache (bool): Whether to use the cache.
        debug (bool): Whether to enable debug logging.

    """
    if debug:
        logging.basicConfig(level=logging.INFO)

    App.load_app_state()
    app_state = AppState.get()
    video = app_state.youtube_facade.get_video(video_id, use_cache=use_cache)
    print_video(video)


@main.command(name="record")
@click.argument("record_id", type=str)
@click.option("--debug", type=bool, default=False, is_flag=True)
def get_record(
    record_id: str,
    debug: bool = False,
) -> None:
    """Get a record by ID.

    Args:
        record_id (str): The ID of the record to get.
        debug (bool): Whether to enable debug logging.

    Raises:
        ValueError: If the record with the given ID is not found.

    """
    if debug:
        logging.basicConfig(level=logging.INFO)

    App.load_app_state()
    app_state = AppState.get()
    records = app_state.record_tracker.load()
    for record in records:
        if record.id == record_id:
            for choice in record.choice_set.choices:
                video_id = choice.video_id
                for video in app_state.youtube_facade.iter_videos([video_id]):
                    print(f"{video.id}: ({choice.action}) {video.title}")
            break
    else:
        msg = f"Record with ID {record_id} not found"
        raise ValueError(msg)


@main.command(name="playlist")
@click.argument("playlist_id", type=str)
@click.option("--use-cache/--no-cache", default=True)
@click.option("--debug", type=bool, default=False, is_flag=True)
@click.option("--n-videos", type=int, default=0)
def get_playlist(
    playlist_id: str,
    use_cache: bool,
    debug: bool = False,
    n_videos: int = 0,
) -> None:
    """Get playlist information.

    Args:
        playlist_id (str): The ID of the playlist to get information for.
        use_cache (bool): Whether to use the cache.
        debug (bool): Whether to enable debug logging.
        n_videos (int): The number of videos to display.

    """
    if debug:
        logging.basicConfig(level=logging.INFO)

    App.load_app_state()
    app_state = AppState.get()
    playlist = app_state.youtube_facade.get_playlist(playlist_id, use_cache=use_cache)
    print_playlist(playlist)

    if n_videos > 0:
        items = sorted(playlist.items, key=lambda x: x.added_at, reverse=True)
        for item in islice(items, n_videos):
            video = app_state.youtube_facade.get_video(item.video_id)
            print("= = = = = = = = = = = =")
            print_video(video)


@main.command(name="channel")
@click.argument("channel_id", type=str)
@click.option("--use-cache/--no-cache", default=True)
@click.option("--debug", type=bool, default=False, is_flag=True)
def get_channel(
    channel_id: str,
    use_cache: bool,
    debug: bool = False,
) -> None:
    """Get channel information.

    Args:
        channel_id (str): The ID of the channel to get information for.
        use_cache (bool): Whether to use the cache.
        debug (bool): Whether to enable debug logging.

    """
    if debug:
        logging.basicConfig(level=logging.INFO)

    App.load_app_state()
    app_state = AppState.get()
    channel = app_state.youtube_facade.get_channel(channel_id, use_cache=use_cache)
    print_channel(channel)


@main.command(name="analyze")
def analyze_records() -> None:
    """Analyze the distribution of records."""
    App.load_app_state()
    app_state = AppState.get()
    records = app_state.record_tracker.load()
    print_ratings_histogram(records, app_state.youtube_facade)


@main.command(name="cache")
def cache_info() -> None:
    """Print cache summary information."""
    App.load_app_state()
    app_state = AppState.get()
    records = app_state.record_tracker.load()
    print(f"Total records: {len(records)}")

    video_ids = set()
    for record in records:
        for choice in record.choice_set.choices:
            if choice.action in [Action.SELECT, Action.NOTHING]:
                video_ids.add(choice.video_id)
    print(f"Unique videos processed: {len(video_ids)}")

    print(f"Cached videos: {len(app_state.youtube_facade.video_cache)}")
    print(f"Cached channels: {len(app_state.youtube_facade.channel_cache)}")
    print(f"Cached playlists: {len(app_state.youtube_facade.playlist_cache)}")


@main.command(name="rank")
@click.option("--n", type=int, default=10)
def rank_videos(n: int = 10) -> None:
    """Rank videos.

    Args:
        n (int): The number of videos to calculate rankings for.

    """
    App.load_app_state()
    app_state = AppState.get()
    records = app_state.record_tracker.load()
    rankings = Ranker.iter_rankings(records)

    for ranking in islice(rankings, n):
        video = app_state.youtube_facade.get_video(ranking.video_id)

        print(f"{video.title}")
        print(f"{url_from_video_id(video.id)}")
        print("= = = = = = = = = = = =")
        print()
