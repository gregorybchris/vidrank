import logging
from typing import Any

import click

from vidrank.app.app import App
from vidrank.app.app_state import AppState

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


@main.command()
@click.argument("record_id", type=str)
def record(record_id: str) -> None:
    App.load_app_state()
    app_state = AppState.get()
    records = app_state.record_tracker.load()
    for r in records:
        if r.id == record_id:
            for choice in r.choice_set.choices:
                video_id = choice.video_id
                for video in app_state.youtube_facade.iter_videos([video_id]):
                    print(f"{video.id}: ({choice.action}) {video.title}")
            break
    else:
        logger.error(f"Record with ID {record_id} not found")
