from dataclasses import dataclass
from typing import Iterator

from trueskill import Rating, rate

from vidrank.lib.models.action import Action
from vidrank.lib.models.record import Record
from vidrank.lib.ranking.ranking import Ranking


@dataclass
class Comp:
    """A comparison between two videos."""

    winner_id: str
    loser_id: str


class Ranker:
    """Video ranker.

    Uses treuskill scores to rank videos based on pairwise comparisons.
    """

    @classmethod
    def iter_rankings(cls, records: list[Record]) -> Iterator[Ranking]:
        """Iterate over the rankings of the videos.

        Args:
            records (list[Record]): The records of the user choices.

        Yields:
            Iterator[Ranking]: An iterator over the rankings of the videos.
        """
        rating_map: dict[str, Rating] = {}
        for comp in cls._get_comps(records):
            cls._update_ratings(rating_map, comp)

        sorted_ratings = sorted(rating_map.items(), key=lambda x: x[1].mu, reverse=True)
        for i, (video_id, rating) in enumerate(sorted_ratings):
            yield Ranking(video_id=video_id, rank=i + 1, rating=rating.mu)

    @classmethod
    def _update_ratings(cls, rating_map: dict[str, Rating], comp: Comp) -> None:
        for video_id in [comp.winner_id, comp.loser_id]:
            if video_id not in rating_map:
                rating_map[video_id] = Rating()

        winner_rating = rating_map[comp.winner_id]
        loser_rating = rating_map[comp.loser_id]

        rating_groups = [{comp.winner_id: winner_rating}, {comp.loser_id: loser_rating}]
        comp_ratings = rate(rating_groups, ranks=[0, 1])
        rating_map.update(comp_ratings[0])
        rating_map.update(comp_ratings[1])

    @classmethod
    def _get_comps(cls, records: list[Record]) -> Iterator[Comp]:
        for record in records:
            for choice_a in record.choice_set.choices:
                action_a = choice_a.action
                for choice_b in record.choice_set.choices:
                    action_b = choice_b.action

                    if (action_a, action_b) == (Action.SELECT, Action.NOTHING):
                        yield Comp(choice_a.video_id, choice_b.video_id)
                    if (action_a, action_b) == (Action.NOTHING, Action.SELECT):
                        yield Comp(choice_b.video_id, choice_a.video_id)
