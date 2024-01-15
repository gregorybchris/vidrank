from typing import List, Tuple

from vidrank.lib.record import Record
from vidrank.lib.youtube.video import Video
from vidrank.lib.youtube_facade import YouTubeFacade


class Ranker:
    @classmethod
    def rank(cls, records: List[Record], *, youtube_facade: YouTubeFacade) -> List[Video]:
        constraints: List[Tuple[str, str]] = []
        video_ids = set()
        to_remove = set()
        for record in records:
            for video_a in record.selection.videos:
                video_ids.add(video_a.video_id)
                action_a = video_a.action
                if action_a == "remove":
                    to_remove.add(video_a.video_id)
                    continue
                for video_b in record.selection.videos:
                    action_b = video_b.action
                    if action_b == "remove":
                        continue

                    if (action_a, action_b) == ("select", "nothing"):
                        constraints.append((video_a.video_id, video_b.video_id))
                    if (action_a, action_b) == ("nothing", "select"):
                        constraints.append((video_b.video_id, video_a.video_id))

        selected_ids = set()
        for video_id, _ in constraints:
            selected_ids.add(video_id)

        videos = []
        for video in youtube_facade.iter_videos(list(selected_ids)):
            videos.append(video)

        return videos
        # TODO: Implement better ranking
