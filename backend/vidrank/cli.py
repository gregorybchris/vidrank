import logging
from typing import Any

import click

from vidrank.app import App

logger = logging.getLogger(__name__)


@click.group()
def main() -> None:
    """Main CLI entrypoint."""


@main.command()
@click.option("--host", "host", type=str, default=App.DEFAULT_HOST)
@click.option("--port", "port", type=int, default=App.DEFAULT_PORT)
def serve(**kwds: Any) -> None:
    with App.context(**kwds) as api:
        api.start()
