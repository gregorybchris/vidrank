import logging
import math
from typing import ClassVar, Iterator, Mapping, Optional

from httpx import Client as HttpClient

from vidrank.lib.youtube.channel import Channel
from vidrank.lib.youtube.playlist import Playlist
from vidrank.lib.youtube.playlist_item import PlaylistItem
from vidrank.lib.youtube.video import Video
from vidrank.lib.youtube.youtube_marshaller import YouTubeMarshaller

logger = logging.getLogger(__name__)


class YouTubeClient:
    """Client for the YouTube API."""

    VIDEO_PARTS: ClassVar[list[str]] = [
        "id",
        "contentDetails",
        "player",
        "snippet",
        "statistics",
        "status",
        "topicDetails",
    ]

    PLAYLIST_PARTS: ClassVar[list[str]] = [
        "id",
        "snippet",
        "contentDetails",
    ]

    BASE_URL = "https://www.googleapis.com/youtube/v3"

    DEFAULT_BATCH_SIZE = 50

    def __init__(self, api_key: str, *, batch_size: int = DEFAULT_BATCH_SIZE):
        """Initialize the YouTubeClient.

        Args:
            api_key (str): The API key for the YouTube API.
            batch_size (int): The number of items to request in each batch.
        """
        self.api_key = api_key
        self.batch_size = batch_size
        self.http_client = HttpClient()

    def iter_videos(self, video_ids: list[str], timeout: Optional[int] = None) -> Iterator[Video]:
        """Iterate over videos by their IDs.

        Args:
            video_ids (list[str]): The IDs of the videos to fetch.
            timeout (int): The timeout for the request.

        Returns:
            Iterator[Video]: An iterator over the videos.

        Raises:
            ValueError: If the API request fails.
        """
        n_chunks = math.ceil(len(video_ids) / self.batch_size)
        for chunk_i in range(0, n_chunks):
            chunk_ids = video_ids[chunk_i * self.batch_size : (chunk_i + 1) * self.batch_size]

            logger.debug("Requesting %d videos from the YouTube API.", len(chunk_ids))

            concat_ids = ",".join(chunk_ids)
            params: Mapping[str, str | int | list[str]] = {
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

                logger.debug("Request URL: %s", response.request.url)

                response_json = response.json()
                if "error" in response_json:
                    raise ValueError(response_json["error"]["message"])

                for response_item in response_json["items"]:
                    yield YouTubeMarshaller.parse_video(response_item)

                if "nextPageToken" in response_json:
                    page_token = response_json["nextPageToken"]
                else:
                    break

    def get_channel(self, channel_id: str, timeout: Optional[int] = None) -> Channel:
        """Get a channel by its ID.

        Args:
            channel_id (str): The ID of the channel to fetch.
            timeout (int): The timeout for the request.

        Returns:
            Channel: The channel with the given ID.

        Raises:
            ValueError: If the API request fails.
        """
        params: Mapping[str, str | int | list[str]] = {
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
        logger.debug("Request URL: %s", response.request.url)

        response_json = response.json()
        if "error" in response_json:
            raise ValueError(response_json["error"]["message"])
        if response_json["pageInfo"]["totalResults"] == 0:
            msg = f"Channel with ID {channel_id} not found"
            raise ValueError(msg)

        response_item = response_json["items"][0]
        return YouTubeMarshaller.parse_channel(response_item)

    def get_playlist(self, playlist_id: str, timeout: Optional[int] = None) -> Playlist:
        """Get a playlist by its ID.

        Args:
            playlist_id (str): The ID of the playlist to fetch.
            timeout (int): The timeout for the request.

        Returns:
            Playlist: The playlist with the given ID.

        Raises:
            ValueError: If the API request fails.
        """
        params: Mapping[str, str | int | list[str]] = {
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
        logger.debug("Request URL: %s", response.request.url)

        response_json = response.json()
        if "error" in response_json:
            raise ValueError(response_json["error"]["message"])
        if response_json["pageInfo"]["totalResults"] == 0:
            msg = f"Playlist with ID {playlist_id} not found"
            raise ValueError(msg)

        items = list(self._iter_playlist_items(playlist_id, timeout=timeout))
        response_item = response_json["items"][0]
        return YouTubeMarshaller.parse_playlist(response_item, items)

    def _iter_playlist_items(self, playlist_id: str, timeout: Optional[int] = None) -> Iterator[PlaylistItem]:
        params: Mapping[str, str | int | list[str]] = {
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
            logger.debug("Request URL: %s", response.request.url)

            response_json = response.json()
            if "error" in response_json:
                not_found_code = 404
                if response_json["error"]["code"] == not_found_code:
                    msg = f"Playlist with ID {playlist_id} not found"
                    raise ValueError(msg)
                raise ValueError(response_json["error"]["message"])

            for response_item in response_json["items"]:
                yield YouTubeMarshaller.parse_playlist_item(response_item)

            if "nextPageToken" in response_json:
                page_token = response_json["nextPageToken"]
            else:
                break
