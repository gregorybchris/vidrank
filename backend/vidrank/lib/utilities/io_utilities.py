from vidrank.lib.youtube.channel import Channel
from vidrank.lib.youtube.video import Video


def print_video(video: Video) -> None:
    print(f"ID: {video.id}")
    print(f"URL: https://www.youtube.com/watch?v={video.id}")
    print(f"Title: {video.title}")
    print(f"Duration: {video.duration}")
    print(f"Channel ID: {video.channel_id}")
    print(f"Channel: {video.channel}")
    print(f"Publish datetime: {video.publish_datetime.to_day_datetime_string()}")
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
    print(f"ID: {channel.id}")
    print(f"URL: {channel.url}")
    print(f"Name: {channel.name}")
    thumbnail = channel.thumbnails.get_highest_resolution()
    if thumbnail is not None:
        print(f"Thumbnail URL: {thumbnail.url}")
    print("Stats: ")
    print(f"\tSubscribers: {channel.stats.subscribers}")
    print(f"\tVideos: {channel.stats.videos}")
    print(f"\tViews: {channel.stats.views}")
