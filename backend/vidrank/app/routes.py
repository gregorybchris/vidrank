from itertools import islice

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from vidrank import __version__ as package_version
from vidrank.app.app_state import AppState
from vidrank.lib.selection import Selection
from vidrank.lib.transaction import Transaction
from vidrank.lib.transaction_type import TransactionType

router = APIRouter()


@router.get(name="Status", description="Get the API status.", path="/")
def get_status() -> JSONResponse:
    return JSONResponse({"status": "healthy"})


@router.get(name="Version", description="Get the API version.", path="/version")
def get_version() -> JSONResponse:
    return JSONResponse({"version": package_version})


@router.get(name="Videos", description="Get videos.", path="/videos")
def get_videos() -> JSONResponse:
    app_state = AppState.get()
    # playlist = app_state.youtube_facade.get_playlist("PL0KIGdjEQDyHGXlhUMndOPherxDmXDQxn", "Next")
    playlist = app_state.youtube_facade.get_playlist("PL0KIGdjEQDyFs9G4IWU8cbdGQuIGjCWYV", "Cooking")

    n_videos = 6
    playlist_video_ids = playlist.video_ids
    video_ids = app_state.rng.choice(playlist_video_ids, n_videos, replace=False)
    video_iterator = app_state.youtube_facade.iter_videos(video_ids)
    videos = list(video_iterator)

    return JSONResponse({"videos": [video.serialize() for video in videos]})


@router.post(name="Submit", description="Post submit.", path="/submit")
def post_submit(selection: Selection) -> JSONResponse:
    app_state = AppState.get()
    transaction = Transaction(
        transaction_type=TransactionType.SUBMIT,
        selection=selection,
    )
    app_state.transaction_tracker.add(transaction)
    return JSONResponse({"result": "submitted"})


@router.post(name="Undo", description="Post undo.", path="/undo")
def post_undo() -> JSONResponse:
    return JSONResponse({"result": "undone"})


@router.post(name="Skip", description="Post skip.", path="/skip")
def post_skip() -> JSONResponse:
    return JSONResponse({"result": "skipped"})
