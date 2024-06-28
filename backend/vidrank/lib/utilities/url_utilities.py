"""Utility functions for YouTube URLs."""


def url_from_video_id(video_id: str) -> str:
    """Return the URL for a YouTube video given its ID.

    Args:
    ----
    video_id (str): The ID of the video.

    Returns:
    -------
    str: The URL for the video.

    """
    return f"https://www.youtube.com/watch?v={video_id}"


def url_from_channel_id(channel_id: str) -> str:
    """Return the URL for a YouTube channel given its ID.

    Args:
    ----
    channel_id (str): The ID of the channel.

    Returns:
    -------
    str: The URL for the channel.

    """
    return f"https://www.youtube.com/channel/{channel_id}"


def url_from_playlist_id(playlist_id: str) -> str:
    """Return the URL for a YouTube playlist given its ID.

    Args:
    ----
    playlist_id (str): The ID of the playlist.

    Returns:
    -------
    str: The URL for the playlist.

    """
    return f"https://www.youtube.com/playlist?list={playlist_id}"
