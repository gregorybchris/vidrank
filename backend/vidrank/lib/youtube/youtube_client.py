import logging
import math
from typing import Iterator, List, Mapping, Optional

from httpx import Client as HttpClient

from vidrank.lib.youtube.video import Video

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
        "contentDetails",
    ]

    BASE_URL = "https://www.googleapis.com/youtube/v3/"

    BATCH_SIZE = 50

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.http_client = HttpClient()

    # pylint: disable=redefined-builtin
    def iter_videos(self, video_ids: List[str], timeout: Optional[int] = None) -> Iterator[Video]:
        logger.debug("Making request to YouTube API.")

        n_chunks = math.ceil(len(video_ids) / self.BATCH_SIZE)
        for chunk_i in range(0, n_chunks):
            chunk_ids = video_ids[chunk_i * self.BATCH_SIZE : (chunk_i + 1) * self.BATCH_SIZE]
            concat_ids = ",".join(chunk_ids)
            params: Mapping[str, str | int | List[str]] = {
                "id": concat_ids,
                "key": self.api_key,
                "hl": "en_US",
                "part": self.VIDEO_PARTS,
                "maxResults": self.BATCH_SIZE,
            }

            page_token = None
            while True:
                request_params = {**params}
                if page_token is not None:
                    request_params["pageToken"] = page_token

                request_url = self.BASE_URL + "videos"
                response = self.http_client.get(
                    request_url,
                    params=request_params,
                    timeout=timeout,
                )

                logger.info("Request URL: %s" % response.request.url)

                response_json = response.json()
                if "error" in response_json:
                    raise ValueError(response_json["error"]["message"])

                videos = [Video.from_dict(d) for d in response_json["items"]]
                yield from videos

                if "nextPageToken" in response_json:
                    page_token = response_json["nextPageToken"]
                else:
                    break

    def iter_playlist_video_ids(self, playlist_id: str, timeout: Optional[int] = None) -> Iterator[str]:
        params: Mapping[str, str | int | List[str]] = {
            "playlistId": playlist_id,
            "key": self.api_key,
            "hl": "en_US",
            "part": self.PLAYLIST_PARTS,
            "maxResults": 50,
        }

        page_token = None
        while True:
            request_params = {**params}
            if page_token is not None:
                request_params["pageToken"] = page_token

            request_url = self.BASE_URL + "playlistItems"
            response = self.http_client.get(
                request_url,
                timeout=timeout,
                params=request_params,
            )
            logger.info("Request URL: %s" % response.request.url)

            response_json = response.json()

            if "error" in response_json:
                raise ValueError(response_json["error"]["message"])

            for item in response_json["items"]:
                yield item["contentDetails"]["videoId"]

            if "nextPageToken" in response_json:
                page_token = response_json["nextPageToken"]
            else:
                break
