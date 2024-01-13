import os

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from vidrank import __version__ as package_version
from vidrank.lib.youtube.video import Video
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

    client = YouTubeClient(api_key)
    video_ids = [
        "ezOIBfZcwbQ",  # All-In
        "DNIvycJd6oM",  # Winklevoss
    ]
    videos = client.get_videos(video_ids)

    for video in videos:
        print("===========")
        print_video(video)

    return JSONResponse({"videos": []})


def print_video(video: Video) -> None:
    print(f"ID: {video.id}")
    print(f"URL: https://www.youtube.com/watch?v={video.id}")
    print(f"Title: {video.title}")
    print(f"Duration: {video.duration}")
    print(f"Channel: {video.channel}")
    print(f"Publish datetime: {video.publish_datetime.to_day_datetime_string()}")
    # print(f"Tags: {video.tags}")
    thumbnail = video.thumbnails.get_highest_resolution()
    if thumbnail is not None:
        print(f"Thumbnail URL: {thumbnail.url}")
    print("Stats: ")
    print(f"\tViews: {video.stats.n_views}")
    print(f"\tFavorites: {video.stats.n_favorites}")
    print(f"\tLikes: {video.stats.n_likes}")
    print(f"\tDislikes: {video.stats.n_dislikes}")
    print(f"\tComments: {video.stats.n_comments}")
