import os
from itertools import islice
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from vidrank import __version__ as package_version
from vidrank.lib.playlist_cache import PlaylistCache
from vidrank.lib.video_cache import VideoCache
from vidrank.lib.video_utilities import print_video
from vidrank.lib.youtube.youtube_client import YouTubeClient
from vidrank.lib.youtube_facade import YouTubeFacade

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
    youtube_client = YouTubeClient(api_key)
    video_cache = VideoCache(cache_dirpath)
    playlist_cache = PlaylistCache(cache_dirpath)
    youtube_facade = YouTubeFacade(
        youtube_client=youtube_client,
        video_cache=video_cache,
        playlist_cache=playlist_cache,
    )

    # playlist = youtube_facade.get_playlist("PL0KIGdjEQDyHGXlhUMndOPherxDmXDQxn", "Next")
    # playlist = youtube_facade.get_playlist("PL0KIGdjEQDyG2nMJRAevxBohq-Nschpma", "Hardware")
    playlist = youtube_facade.get_playlist("PL0KIGdjEQDyFs9G4IWU8cbdGQuIGjCWYV", "Cooking")

    n_videos = 6
    video_ids = playlist.video_ids
    video_iterator = youtube_facade.iter_videos(video_ids)
    videos = list(islice(video_iterator, n_videos))

    for video in videos:
        print("===========")
        print_video(video)

    return JSONResponse({"videos": [video.serialize() for video in videos]})


@router.post(name="Select", description="Post selection.", path="/select")
def post_select() -> JSONResponse:
    return JSONResponse({"result": "selected"})
