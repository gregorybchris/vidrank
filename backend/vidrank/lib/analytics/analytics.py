# ruff: noqa: T201
from vidrank.lib.models.action import Action
from vidrank.lib.models.record import Record
from vidrank.lib.youtube.playlist import Playlist
from vidrank.lib.youtube.youtube_facade import YouTubeFacade


def print_analysis(records: list[Record], playlist: Playlist, youtube_facade: YouTubeFacade) -> None:
    """Print stats about the completed records.

    Args:
        records (list[Record]): The records to analyze.
        playlist (Playlist): The YouTube playlist.
        youtube_facade (YouTubeFacade): The YouTube facade.
    """
    n_videos = len(playlist.items)
    print(f"A total of {n_videos} videos are in the playlist.")

    print(f"A total of {len(records)} records have been created.")

    video_ids = set()

    counts: dict[str, dict[str, int]] = {}
    for record in records:
        for choice in record.choice_set.choices:
            video_id = choice.video_id

            if choice.action in [Action.SELECT, Action.NOTHING]:
                video_ids.add(video_id)

            if video_id not in counts:
                counts[video_id] = {}
            if choice.action not in counts[video_id]:
                counts[video_id][choice.action] = 0
            counts[video_id][choice.action] += 1

    print(f"A total of {len(video_ids)} unique videos have been rated.")

    n_comps = 0
    for record in records:
        for choice_a in record.choice_set.choices:
            for choice_b in record.choice_set.choices:
                action_a = choice_a.action
                action_b = choice_b.action

                if (action_a, action_b) == (Action.SELECT, Action.NOTHING):
                    n_comps += 1

    print(f"A total of {n_comps} pairs of videos have been compared.")

    print()
    print("Videos with the most selections:")

    for video_id, ratings in sorted(counts.items(), key=lambda x: x[1].get(Action.SELECT, 0), reverse=True):
        select_count = ratings.get(Action.SELECT, 0)
        min_select_count = 4
        if select_count >= min_select_count:
            video = youtube_facade.get_video(video_id)
            print(f"{select_count}: {video.title}")
