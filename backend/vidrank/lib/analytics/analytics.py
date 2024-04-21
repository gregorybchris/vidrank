from typing import Dict, List

from vidrank.lib.action import Action
from vidrank.lib.record import Record
from vidrank.lib.youtube_facade import YouTubeFacade


def print_ratings_histogram(records: List[Record], youtube_facade: YouTubeFacade) -> None:
    print(f"A total of {len(records)} records have been created.")

    counts: Dict[str, Dict[str, int]] = {}
    for record in records:
        for choice in record.choice_set.choices:
            video_id = choice.video_id
            if video_id not in counts:
                counts[video_id] = {}
            if choice.action not in counts[video_id]:
                counts[video_id][choice.action] = 0
            counts[video_id][choice.action] += 1

    for video_id, ratings in sorted(counts.items(), key=lambda x: x[1].get(Action.SELECT, 0), reverse=True):
        select_count = ratings.get(Action.SELECT, 0)
        if select_count > 2:
            video = youtube_facade.get_video(video_id)
            print(f"{select_count}: {video.title}")
