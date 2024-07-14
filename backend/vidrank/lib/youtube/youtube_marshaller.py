import logging
from typing import Optional, cast

from pydantic_extra_types.pendulum_dt import DateTime, Duration
from pydantic_extra_types.pendulum_dt import parse as pendulum_parse

from vidrank.lib.utilities.typing_utilities import JsonObject
from vidrank.lib.youtube.channel import Channel
from vidrank.lib.youtube.channel_stats import ChannelStats
from vidrank.lib.youtube.playlist import Playlist
from vidrank.lib.youtube.playlist_item import PlaylistItem
from vidrank.lib.youtube.thumbnail import Thumbnail
from vidrank.lib.youtube.thumbnail_set import ThumbnailSet
from vidrank.lib.youtube.video import Video
from vidrank.lib.youtube.video_stats import VideoStats

logger = logging.getLogger(__name__)


class YouTubeMarshaller:
    """Marshaller for YouTube API JSON."""

    @classmethod
    def parse_video(cls, video_dict: JsonObject) -> Video:
        """Parse a Video from YouTube API JSON.

        Args:
            video_dict (JsonObject): The JSON object representing the video.

        Returns:
            Video: The parsed video.
        """
        duration = pendulum_parse(video_dict["contentDetails"]["duration"])
        published_at = pendulum_parse(video_dict["snippet"]["publishedAt"])
        return Video(
            id=video_dict["id"],
            title=video_dict["snippet"]["title"],
            description=video_dict["snippet"]["description"],
            duration=cast(Duration, duration),
            channel_id=video_dict["snippet"]["channelId"],
            channel=video_dict["snippet"]["channelTitle"],
            published_at=cast(DateTime, published_at),
            thumbnails=cls.parse_thumbnail_set(video_dict["snippet"]["thumbnails"]),
            stats=cls.parse_video_stats(video_dict["statistics"]),
        )

    @classmethod
    def parse_thumbnail_set(cls, thumbnail_set_dict: JsonObject) -> ThumbnailSet:
        """Parse a ThumbnailSet from YouTube API JSON.

        Args:
            thumbnail_set_dict (JsonObject): The JSON object representing the thumbnail set.

        Returns:
            ThumbnailSet: The parsed thumbnail set.
        """
        thumbnail_set_kwargs: dict[str, Optional[Thumbnail]] = {}
        for size in ["default", "standard", "medium", "high", "maxres"]:
            if size in thumbnail_set_dict and thumbnail_set_dict[size] is not None:
                thumbnail_dict = thumbnail_set_dict[size]
                thumbnail = Thumbnail(
                    width=thumbnail_dict["width"],
                    height=thumbnail_dict["height"],
                    url=thumbnail_dict["url"],
                )
                thumbnail_set_kwargs[size] = thumbnail
            else:
                thumbnail_set_kwargs[size] = None
        return ThumbnailSet(**thumbnail_set_kwargs)

    @classmethod
    def parse_video_stats(cls, stats_dict: JsonObject) -> VideoStats:
        """Parse VideoStats from YouTube API JSON.

        Args:
            stats_dict (JsonObject): The JSON object representing the video stats.

        Returns:
            VideoStats: The parsed video stats.
        """
        stats_kwargs = {}
        stat_map = {
            "favoriteCount": "n_favorites",
            "commentCount": "n_comments",
            "dislikeCount": "n_dislikes",
            "likeCount": "n_likes",
            "viewCount": "n_views",
        }
        for youtube_stat, video_stat in stat_map.items():
            if youtube_stat not in stats_dict:
                stats_dict[youtube_stat] = 0
            stats_kwargs[video_stat] = stats_dict[youtube_stat]
        return VideoStats(**stats_kwargs)

    @classmethod
    def parse_channel(cls, channel_dict: JsonObject) -> Channel:
        """Parse a Channel from YouTube API JSON.

        Args:
            channel_dict (JsonObject): The JSON object representing the channel.

        Returns:
            Channel: The parsed channel.
        """
        channel_id = channel_dict["id"]
        return Channel(
            id=channel_id,
            name=channel_dict["snippet"]["title"],
            thumbnails=YouTubeMarshaller.parse_thumbnail_set(channel_dict["snippet"]["thumbnails"]),
            stats=YouTubeMarshaller.parse_channel_stats(channel_dict["statistics"]),
        )

    @classmethod
    def parse_channel_stats(cls, stats_dict: JsonObject) -> ChannelStats:
        """Parse ChannelStats from YouTube API JSON.

        Args:
            stats_dict (JsonObject): The JSON object representing the channel stats.

        Returns:
            ChannelStats: The parsed channel stats.
        """
        return ChannelStats(
            subscribers=stats_dict["subscriberCount"],
            videos=stats_dict["videoCount"],
            views=stats_dict["viewCount"],
        )

    @classmethod
    def parse_playlist(cls, playlist_dict: JsonObject, items: list[PlaylistItem]) -> Playlist:
        """Parse a Playlist from YouTube API JSON.

        Args:
            playlist_dict (JsonObject): The JSON object representing the playlist.
            items (list[PlaylistItem]): The items in the playlist.

        Returns:
            Playlist: The parsed playlist.
        """
        playlist_id = playlist_dict["id"]
        created_at = pendulum_parse(playlist_dict["snippet"]["publishedAt"])
        return Playlist(
            id=playlist_id,
            title=playlist_dict["snippet"]["title"],
            created_at=cast(DateTime, created_at),
            thumbnails=cls.parse_thumbnail_set(playlist_dict["snippet"]["thumbnails"]),
            description=playlist_dict["snippet"]["description"],
            items=items,
        )

    @classmethod
    def parse_playlist_item(cls, playlist_item_dict: JsonObject) -> PlaylistItem:
        """Parse a PlaylistItem from YouTube API JSON.

        Args:
            playlist_item_dict (JsonObject): The JSON object representing the playlist item.

        Returns:
            PlaylistItem: The parsed playlist item.
        """
        video_id = playlist_item_dict["contentDetails"]["videoId"]
        added_at = pendulum_parse(playlist_item_dict["snippet"]["publishedAt"])
        return PlaylistItem(
            video_id=video_id,
            added_at=cast(DateTime, added_at),
            position=playlist_item_dict["snippet"]["position"],
            title=playlist_item_dict["snippet"]["title"],
            description=playlist_item_dict["snippet"]["description"],
            thumbnails=cls.parse_thumbnail_set(playlist_item_dict["snippet"]["thumbnails"]),
        )
