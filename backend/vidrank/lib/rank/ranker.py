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
            for choice_a in record.choice_set.choices:
                video_ids.add(choice_a.video_id)
                action_a = choice_a.action
                if action_a == "remove":
                    to_remove.add(choice_a.video_id)
                    continue
                for choice_b in record.choice_set.choices:
                    action_b = choice_b.action
                    if action_b == "remove":
                        continue

                    if (action_a, action_b) == ("select", "nothing"):
                        constraints.append((choice_a.video_id, choice_b.video_id))
                    if (action_a, action_b) == ("nothing", "select"):
                        constraints.append((choice_b.video_id, choice_a.video_id))

        selected_ids = set()
        for video_id, _ in constraints:
            selected_ids.add(video_id)

        videos = []
        for video in youtube_facade.iter_videos(list(selected_ids)):
            videos.append(video)

        return videos
        # TODO: Implement better ranking
