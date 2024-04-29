import logging
from typing import Any

import click

from vidrank.app.app import App
from vidrank.app.app_state import AppState
from vidrank.lib.analytics.analytics import print_ratings_histogram
from vidrank.lib.utilities.io_utilities import print_channel, print_video

logger = logging.getLogger(__name__)


@click.group()
def main() -> None:
    """Main CLI entrypoint."""


@main.command()
@click.option("--host", "host", type=str, default=App.DEFAULT_HOST)
@click.option("--port", "port", type=int, default=App.DEFAULT_PORT)
@click.option("--debug", type=bool, default=False, is_flag=True)
def serve(debug: bool = False, **kwds: Any) -> None:
    if debug:
        logging.basicConfig(level=logging.INFO)

    with App.context(**kwds) as app:
        app.start()


@main.command(name="video")
@click.argument("video_id", type=str)
@click.option("--use-cache/--no-cache", default=True)
def get_video(video_id: str, use_cache: bool) -> None:
    App.load_app_state()
    app_state = AppState.get()
    video = app_state.youtube_facade.get_video(video_id, use_cache=use_cache)
    print_video(video)


@main.command(name="record")
@click.argument("record_id", type=str)
def get_record(record_id: str) -> None:
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
        raise ValueError(f"Record with ID {record_id} not found")


@main.command(name="playlist")
@click.argument("playlist_id", type=str)
@click.option("--use-cache/--no-cache", default=True)
def get_playlist(playlist_id: str, use_cache: bool) -> None:
    App.load_app_state()
    app_state = AppState.get()
    playlist = app_state.youtube_facade.get_playlist(playlist_id, use_cache=use_cache)
    print(f"Loaded playlist: {playlist_id} with {len(playlist.items)} videos")


@main.command(name="channel")
@click.argument("channel_id", type=str)
@click.option("--use-cache/--no-cache", default=True)
def get_channel(channel_id: str, use_cache: bool) -> None:
    App.load_app_state()
    app_state = AppState.get()
    channel = app_state.youtube_facade.get_channel(channel_id, use_cache=use_cache)
    print_channel(channel)


@main.command(name="analyze")
def analyze_records() -> None:
    App.load_app_state()
    app_state = AppState.get()
    records = app_state.record_tracker.load()
    print_ratings_histogram(records, app_state.youtube_facade)
