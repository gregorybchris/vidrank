# ruff: noqa: T201
from vidrank.lib.utilities.url_utilities import url_from_channel_id, url_from_playlist_id, url_from_video_id
from vidrank.lib.youtube.channel import Channel
from vidrank.lib.youtube.playlist import Playlist
from vidrank.lib.youtube.video import Video


def print_video(video: Video) -> None:
    """Print YouTube video details to the console.

    Args:
        video (Video): The video to print.
    """
    print(f"ID: {video.id}")
    print(f"URL: {url_from_video_id(video.id)}")
    print(f"Title: {video.title}")
    print(f"Duration: {video.duration}")
    print(f"Channel ID: {video.channel_id}")
    print(f"Channel: {video.channel}")
    print(f"Published at: {video.published_at.to_day_datetime_string()}")
    thumbnail = video.thumbnails.get_highest_resolution()
    if thumbnail is not None:
        print(f"Thumbnail URL: {thumbnail.url}")
    print("Stats: ")
    print(f"\tViews: {video.stats.n_views}")
    print(f"\tFavorites: {video.stats.n_favorites}")
    print(f"\tLikes: {video.stats.n_likes}")
    print(f"\tDislikes: {video.stats.n_dislikes}")
    print(f"\tComments: {video.stats.n_comments}")


def print_channel(channel: Channel) -> None:
    """Print YouTube channel details to the console.

    Args:
        channel (Channel): The channel to print.
    """
    print(f"ID: {channel.id}")
    print(f"URL: {url_from_channel_id(channel.id)}")
    print(f"Name: {channel.name}")
    thumbnail = channel.thumbnails.get_highest_resolution()
    if thumbnail is not None:
        print(f"Thumbnail URL: {thumbnail.url}")
    print("Stats: ")
    print(f"\tSubscribers: {channel.stats.subscribers}")
    print(f"\tVideos: {channel.stats.videos}")
    print(f"\tViews: {channel.stats.views}")


def print_playlist(playlist: Playlist) -> None:
    """Print YouTube playlist details to the console.

    Args:
        playlist (Playlist): The playlist to print.
    """
    print(f"ID: {playlist.id}")
    print(f"URL: {url_from_playlist_id(playlist.id)}")
    print(f"Title: {playlist.title}")
    print(f"Created at: {playlist.created_at.to_day_datetime_string()}")
    thumbnail = playlist.thumbnails.get_highest_resolution()
    if thumbnail is not None:
        print(f"Thumbnail URL: {thumbnail.url}")
    print(f"Description: {playlist.description}")
    print(f"Number of videos: {len(playlist.items)}")
