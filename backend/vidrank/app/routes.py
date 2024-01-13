import os
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from vidrank import __version__ as package_version
from vidrank.lib.video_cache import VideoCache
from vidrank.lib.video_facade import VideoFacade
from vidrank.lib.video_utilities import print_video
from vidrank.lib.youtube.youtube_client import YouTubeClient

router = APIRouter()


@router.get(name="Status", description="Get the API status.", path="/")
def get_status() -> JSONResponse:
    return JSONResponse({"status": "healthy"})


@router.get(name="Version", description="Get the API version.", path="/version")
def get_version() -> JSONResponse:
    return JSONResponse({"version": package_version})


@router.get(name="Videos", description="Get videos.", path="/videos")
def get_videos() -> JSONResponse:
    api_key = os.getenv("YOUTUBE_API_KEY")
    if api_key is None:
        raise ValueError("YOUTUBE_API_KEY environment variable is not set.")

    cache_dir_str = os.getenv("VIDRANK_CACHE_DIR")
    if cache_dir_str is None:
        raise ValueError("VIDRANK_CACHE_DIR environment variable is not set.")

    cache_dirpath = Path(cache_dir_str)
    video_cache = VideoCache(cache_dirpath)
    youtube_client = YouTubeClient(api_key)
    video_facade = VideoFacade(video_cache=video_cache, youtube_client=youtube_client)

    video_ids = [
        # "ezOIBfZcwbQ",  # All-In
        # "DNIvycJd6oM",  # Winklevoss
        "axJtywd9Tbo",
        "3rWsdUkQ_-0",
        "40CB12cj_aM",
        "fLMZAHyrpyo",
        "B2PJh2K-jdU",
        "7s0SzcUnzZo",
    ]

    # playlist_name, playlist_id = "Hardware", "PL0KIGdjEQDyG2nMJRAevxBohq-Nschpma"  # Hardware
    # playlist_name, playlist_id = "Next", "PL0KIGdjEQDyHGXlhUMndOPherxDmXDQxn"  # Next
    playlist_name, playlist_id = "Cooking", "PL0KIGdjEQDyFs9G4IWU8cbdGQuIGjCWYV"  # Cooking

    videos = list(video_facade.iter_playlist_videos(playlist_id))
    # videos = list(video_facade.iter_videos(video_ids))

    for video in videos:
        print("===========")
        print_video(video)

    return JSONResponse({"videos": [video.serialize() for video in videos]})
