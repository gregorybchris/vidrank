import logging
import math
from typing import Dict, Iterator, List, Mapping, Optional, cast

from httpx import Client as HttpClient
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


class YouTubeClient:
    VIDEO_PARTS = [
        "id",
        "contentDetails",
        "player",
        "snippet",
        "statistics",
        "status",
        "topicDetails",
    ]

    PLAYLIST_PARTS = [
        "id",
        "snippet",
        "contentDetails",
    ]

    BASE_URL = "https://www.googleapis.com/youtube/v3"

    DEFAULT_BATCH_SIZE = 50

    def __init__(self, api_key: str, *, batch_size: int = DEFAULT_BATCH_SIZE):
        self.api_key = api_key
        self.http_client = HttpClient()
        self.batch_size = batch_size

    # pylint: disable=redefined-builtin
    def iter_videos(self, video_ids: List[str], timeout: Optional[int] = None) -> Iterator[Video]:
        n_chunks = math.ceil(len(video_ids) / self.batch_size)
        for chunk_i in range(0, n_chunks):
            chunk_ids = video_ids[chunk_i * self.batch_size : (chunk_i + 1) * self.batch_size]

            logger.debug(f"Requesting {len(chunk_ids)} videos from the YouTube API.")

            concat_ids = ",".join(chunk_ids)
            params: Mapping[str, str | int | List[str]] = {
                "id": concat_ids,
                "key": self.api_key,
                "hl": "en_US",
                "part": self.VIDEO_PARTS,
                "maxResults": self.batch_size,
            }

            page_token = None
            while True:
                request_params = {**params}
                if page_token is not None:
                    request_params["pageToken"] = page_token

                request_url = f"{self.BASE_URL}/videos"
                response = self.http_client.get(
                    request_url,
                    params=request_params,
                    timeout=timeout,
                )

                logger.debug(f"Request URL: {response.request.url}")

                response_json = response.json()
                if "error" in response_json:
                    raise ValueError(response_json["error"]["message"])

                for response_item in response_json["items"]:
                    yield ClientMarshaller.parse_video(response_item)

                if "nextPageToken" in response_json:
                    page_token = response_json["nextPageToken"]
                else:
                    break

    def get_channel(self, channel_id: str, timeout: Optional[int] = None) -> Channel:
        params: Mapping[str, str | int | List[str]] = {
            "id": channel_id,
            "key": self.api_key,
            "hl": "en_US",
            "part": ["id", "snippet", "statistics"],
        }

        logger.debug("Requesting channel from the YouTube API.")

        request_url = f"{self.BASE_URL}/channels"
        response = self.http_client.get(
            request_url,
            params=params,
            timeout=timeout,
        )
        logger.debug(f"Request URL: {response.request.url}")

        response_json = response.json()
        if "error" in response_json:
            raise ValueError(response_json["error"]["message"])
        if response_json["pageInfo"]["totalResults"] == 0:
            raise ValueError(f"Channel with ID {channel_id} not found")

        response_item = response_json["items"][0]
        return ClientMarshaller.parse_channel(response_item)

    def get_playlist(self, playlist_id: str, timeout: Optional[int] = None) -> Playlist:
        params: Mapping[str, str | int | List[str]] = {
            "id": playlist_id,
            "key": self.api_key,
            "hl": "en_US",
            "part": ["id", "snippet"],
        }

        logger.debug("Requesting playlist from the YouTube API.")

        request_url = f"{self.BASE_URL}/playlists"
        response = self.http_client.get(
            request_url,
            params=params,
            timeout=timeout,
        )
        logger.debug(f"Request URL: {response.request.url}")

        response_json = response.json()
        if "error" in response_json:
            raise ValueError(response_json["error"]["message"])
        if response_json["pageInfo"]["totalResults"] == 0:
            raise ValueError(f"Playlist with ID {playlist_id} not found")

        items = list(self._iter_playlist_items(playlist_id, timeout=timeout))
        response_item = response_json["items"][0]
        return ClientMarshaller.parse_playlist(response_item, items)

    def _iter_playlist_items(self, playlist_id: str, timeout: Optional[int] = None) -> Iterator[PlaylistItem]:
        params: Mapping[str, str | int | List[str]] = {
            "playlistId": playlist_id,
            "key": self.api_key,
            "hl": "en_US",
            "part": self.PLAYLIST_PARTS,
            "maxResults": self.batch_size,
        }

        page_token = None
        while True:
            request_params = {**params}
            if page_token is not None:
                request_params["pageToken"] = page_token

            logger.debug("Requesting playlist items from the YouTube API.")

            request_url = f"{self.BASE_URL}/playlistItems"
            response = self.http_client.get(
                request_url,
                timeout=timeout,
                params=request_params,
            )
            logger.debug(f"Request URL: {response.request.url}")

            response_json = response.json()
            if "error" in response_json:
                if response_json["error"]["code"] == 404:
                    raise ValueError(f"Playlist with ID {playlist_id} not found")
                raise ValueError(response_json["error"]["message"])

            for response_item in response_json["items"]:
                yield ClientMarshaller.parse_playlist_item(response_item)

            if "nextPageToken" in response_json:
                page_token = response_json["nextPageToken"]
            else:
                break


class ClientMarshaller:

    @classmethod
    def parse_video(cls, video_dict: JsonObject) -> Video:
        duration = pendulum_parse(video_dict["contentDetails"]["duration"])
        published_at = pendulum_parse(video_dict["snippet"]["publishedAt"])
        return Video(
            id=video_dict["id"],
            title=video_dict["snippet"]["title"],
            duration=cast(Duration, duration),
            channel_id=video_dict["snippet"]["channelId"],
            channel=video_dict["snippet"]["channelTitle"],
            published_at=cast(DateTime, published_at),
            thumbnails=cls.parse_thumbnail_set(video_dict["snippet"]["thumbnails"]),
            stats=cls.parse_video_stats(video_dict["statistics"]),
        )

    @classmethod
    def parse_thumbnail_set(cls, thumbnail_set_dict: JsonObject) -> ThumbnailSet:
        thumbnail_set_kwargs: Dict[str, Optional[Thumbnail]] = {}
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
        channel_id = channel_dict["id"]
        return Channel(
            id=channel_id,
            name=channel_dict["snippet"]["title"],
            url=f"https://www.youtube.com/channel/{channel_id}",
            thumbnails=ClientMarshaller.parse_thumbnail_set(channel_dict["snippet"]["thumbnails"]),
            stats=ClientMarshaller.parse_channel_stats(channel_dict["statistics"]),
        )

    @classmethod
    def parse_channel_stats(cls, stats_dict: JsonObject) -> ChannelStats:
        return ChannelStats(
            subscribers=stats_dict["subscriberCount"],
            videos=stats_dict["videoCount"],
            views=stats_dict["viewCount"],
        )

    @classmethod
    def parse_playlist(cls, playlist_dict: JsonObject, items: List[PlaylistItem]) -> Playlist:
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
        video_id = playlist_item_dict["contentDetails"]["videoId"]
        added_at = pendulum_parse(playlist_item_dict["snippet"]["publishedAt"])
        return PlaylistItem(
            video_id=video_id,
            added_at=cast(DateTime, added_at),
        )
