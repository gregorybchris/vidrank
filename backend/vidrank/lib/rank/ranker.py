from typing import List

from vidrank.lib.record import Record
from vidrank.lib.youtube.video import Video
from vidrank.lib.youtube_facade import YouTubeFacade


class Ranker:
    @classmethod
    def rank(cls, records: List[Record], *, youtube_facade: YouTubeFacade) -> List[Video]:
        videos = []
        video_ids = []
        for record in records:
            for selection_video in record.selection.videos:
                video_ids.append(selection_video.video_id)
        for video in youtube_facade.iter_videos(video_ids):
            videos.append(video)
        return videos
        # TODO: Implement better ranking
