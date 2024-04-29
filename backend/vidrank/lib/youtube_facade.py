import logging
from typing import Iterable, Iterator

from vidrank.lib.pickle_cache import PickleCache
from vidrank.lib.youtube.channel import Channel
from vidrank.lib.youtube.playlist import Playlist
from vidrank.lib.youtube.video import Video
from vidrank.lib.youtube.youtube_client import YouTubeClient

logger = logging.getLogger(__name__)


class YouTubeFacade:
    def __init__(
        self,
        *,
        youtube_client: YouTubeClient,
        video_cache: PickleCache[Video],
        channel_cache: PickleCache[Channel],
        playlist_cache: PickleCache[Playlist],
    ):
        self.youtube_client = youtube_client
        self.video_cache = video_cache
        self.channel_cache = channel_cache
        self.playlist_cache = playlist_cache

    def get_video(self, video_id: str, use_cache: bool = True) -> Video:
        if use_cache:
            video = self.video_cache.get(video_id)
            if video is not None:
                return video

        for video in self.youtube_client.iter_videos([video_id]):
            self.video_cache.add(video.id, video)
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
                self.video_cache.add(video.id, video)
                yield video

    def get_channel(self, channel_id: str, use_cache: bool = True) -> Channel:
        if use_cache:
            channel = self.channel_cache.get(channel_id)
            if channel is not None:
                return channel

        channel = self.youtube_client.get_channel(channel_id)
        self.channel_cache.add(channel.id, channel)
        return channel

    def get_playlist(self, playlist_id: str, use_cache: bool = True) -> Playlist:
        if use_cache:
            playlist = self.playlist_cache.get(playlist_id)
            if playlist is not None:
                return playlist

        playlist = self.youtube_client.get_playlist(playlist_id)
        self.playlist_cache.add(playlist.id, playlist)
        return playlist
