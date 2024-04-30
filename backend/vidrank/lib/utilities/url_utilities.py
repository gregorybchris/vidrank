def url_from_video_id(video_id: str) -> str:
    return f"https://www.youtube.com/watch?v={video_id}"


def url_from_channel_id(channel_id: str) -> str:
    return f"https://www.youtube.com/channel/{channel_id}"


def url_from_playlist_id(playlist_id: str) -> str:
    return f"https://www.youtube.com/playlist?list={playlist_id}"
