from typing import List, Mapping, Optional

from httpx import Client as HttpClient

from vidrank.lib.youtube.video import Video


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
    BASE_URL = "https://www.googleapis.com/youtube/v3/"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.http_client = HttpClient()

    # pylint: disable=redefined-builtin
    def get_videos(self, video_ids: List[str], timeout: Optional[int] = None) -> List[Video]:
        id_param = ",".join(video_ids)

        params: Mapping[str, str | List[str]] = {
            "id": id_param,
            "key": self.api_key,
            "hl": "en_US",
            "part": self.VIDEO_PARTS,
        }

        request_url = self.BASE_URL + "videos"
        response = self.http_client.get(
            request_url,
            params=params,
            timeout=timeout,
        )
        response_json = response.json()

        if "error" in response_json:
            raise ValueError(response_json["error"]["message"])

        return [Video.from_dict(d) for d in response_json["items"]]
