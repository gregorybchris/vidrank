import logging
import math
from typing import Iterator, List, Mapping, Optional, cast

from httpx import Client as HttpClient
from pydantic_extra_types.pendulum_dt import DateTime, Duration
from pydantic_extra_types.pendulum_dt import parse as pendulum_parse

from vidrank.lib.utilities.typing_utilities import JsonObject
from vidrank.lib.youtube.playlist_item import PlaylistItem
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
                    yield self._video_from_response(response_item)

                if "nextPageToken" in response_json:
                    page_token = response_json["nextPageToken"]
                else:
                    break

    @classmethod
    def _video_from_response(cls, video_dict: JsonObject) -> "Video":
        duration = pendulum_parse(video_dict["contentDetails"]["duration"])
        publish_datetime = pendulum_parse(video_dict["snippet"]["publishedAt"])
        return Video(
            id=video_dict["id"],
            title=video_dict["snippet"]["title"],
            duration=cast(Duration, duration),
            channel=video_dict["snippet"]["channelTitle"],
            publish_datetime=cast(DateTime, publish_datetime),
            thumbnails=ThumbnailSet.from_dict(video_dict["snippet"]["thumbnails"]),
            stats=VideoStats.from_dict(video_dict["statistics"]),
        )

    def iter_playlist_items(self, playlist_id: str, timeout: Optional[int] = None) -> Iterator[PlaylistItem]:
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
                yield self._playlist_item_from_response(response_item)

            if "nextPageToken" in response_json:
                page_token = response_json["nextPageToken"]
            else:
                break

    @classmethod
    def _playlist_item_from_response(cls, playlist_item_dict: JsonObject) -> "PlaylistItem":
        video_id = playlist_item_dict["contentDetails"]["videoId"]
        added_at = pendulum_parse(playlist_item_dict["snippet"]["publishedAt"])
        return PlaylistItem(
            video_id=video_id,
            added_at=cast(DateTime, added_at),
        )
