import logging
from typing import Iterable, Iterator

from vidrank.lib.playlist_cache import PlaylistCache
from vidrank.lib.video_cache import VideoCache
from vidrank.lib.youtube.playlist import Playlist
from vidrank.lib.youtube.video import Video
from vidrank.lib.youtube.youtube_client import YouTubeClient

logger = logging.getLogger(__name__)


class YouTubeFacade:
    def __init__(
        self,
        *,
        youtube_client: YouTubeClient,
        video_cache: VideoCache,
        playlist_cache: PlaylistCache,
    ):
        self.youtube_client = youtube_client
        self.video_cache = video_cache
        self.playlist_cache = playlist_cache

    def get_video(self, video_id: str, use_cache: bool = True) -> Video:
        if use_cache:
            video = self.video_cache.get(video_id)
            if video is not None:
                return video

        for video in self.youtube_client.iter_videos([video_id]):
            self.video_cache.add(video)
            return video

        raise ValueError(f"Video with ID {video_id} not found")

    def iter_videos(self, video_ids: Iterable[str], use_cache: bool = True) -> Iterator[Video]:
        video_ids_to_fetch = []
        for video_id in video_ids:
            if use_cache:
                video = self.video_cache.get(video_id)
                if video is not None:
                    yield video
                    continue
            video_ids_to_fetch.append(video_id)

        if len(video_ids_to_fetch) != 0:
            for video in self.youtube_client.iter_videos(video_ids_to_fetch):
                self.video_cache.add(video)
                yield video

    def get_playlist(self, playlist_id: str, use_cache: bool = True) -> Playlist:
        if use_cache:
            playlist = self.playlist_cache.get(playlist_id)
            if playlist is not None:
                return playlist

        video_ids = list(self.youtube_client.iter_playlist_video_ids(playlist_id))
        playlist = Playlist(id=playlist_id, video_ids=video_ids)

        self.playlist_cache.add(playlist)

        return playlist
