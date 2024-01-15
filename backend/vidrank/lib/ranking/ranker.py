from dataclasses import dataclass
from typing import Dict, List

from trueskill import Rating, rate

from vidrank.lib.ranking.ranking import Ranking
from vidrank.lib.record import Record


@dataclass
class Comp:
    winner_id: str
    loser_id: str


class Ranker:
    @classmethod
    def rank(cls, records: List[Record]) -> List[Ranking]:
        comps = cls.get_comps(records)

        rating_map: Dict[str, Rating] = {}
        for comp in comps:
            if comp.winner_id not in rating_map:
                rating_map[comp.winner_id] = Rating()
            if comp.loser_id not in rating_map:
                rating_map[comp.loser_id] = Rating()

            winner_rating = rating_map[comp.winner_id]
            loser_rating = rating_map[comp.loser_id]

            rating_groups = [{comp.winner_id: winner_rating}, {comp.loser_id: loser_rating}]
            comp_ratings = rate(rating_groups, ranks=[0, 1])
            rating_map.update(comp_ratings[0])
            rating_map.update(comp_ratings[1])

        rankings = []
        sorted_ratings = sorted(rating_map.items(), key=lambda x: x[1].mu, reverse=True)
        for i, (video_id, rating) in enumerate(sorted_ratings):
            rankings.append(Ranking(video_id=video_id, rank=i + 1, rating=rating.mu))

        return rankings

    @classmethod
    def get_comps(cls, records: List[Record]) -> List[Comp]:
        comps: List[Comp] = []
        for record in records:
            for choice_a in record.choice_set.choices:
                action_a = choice_a.action
                for choice_b in record.choice_set.choices:
                    action_b = choice_b.action

                    if (action_a, action_b) == ("select", "nothing"):
                        comps.append(Comp(choice_a.video_id, choice_b.video_id))
                    if (action_a, action_b) == ("nothing", "select"):
                        comps.append(Comp(choice_b.video_id, choice_a.video_id))
        return comps
