import logging
from typing import Iterator, List

from vidrank.lib.video_cache import VideoCache
from vidrank.lib.youtube.video import Video
from vidrank.lib.youtube.youtube_client import YouTubeClient

logger = logging.getLogger(__name__)


class VideoFacade:
    def __init__(self, *, video_cache: VideoCache, youtube_client: YouTubeClient):
        self.video_cache = video_cache
        self.youtube_client = youtube_client

    def iter_videos(self, video_ids: List[str]) -> Iterator[Video]:
        uncached_ids = []
        for video_id in video_ids:
            video = self.video_cache.get(video_id)

            if video is None:
                uncached_ids.append(video_id)
            else:
                yield video

        if len(uncached_ids) != 0:
            videos = list(self.youtube_client.iter_videos(uncached_ids))
            self.video_cache.add_all(videos)
            yield from videos

    def iter_playlist_videos(self, playlist_id: str) -> Iterator[Video]:
        video_ids = list(self.youtube_client.iter_playlist_video_ids(playlist_id))
        logger.info("Found %s videos in the playlist" % len(video_ids))
        yield from self.iter_videos(video_ids)
