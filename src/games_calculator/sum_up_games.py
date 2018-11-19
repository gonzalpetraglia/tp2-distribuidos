

from collections import Counter
from score import AcummulatedScore
from stateful_processer import StatefulProcesser


class SumUpGames(StatefulProcesser):
    def __init__(self, incoming_address, incoming_port, outgoing_address, outgoing_port, number_of_aggregator):
        def init_state():
            return Counter()
        
        def update_state(games, shot):

            date = shot[0]
            home_team = shot[1]
            away_team = shot[2]
            points = shot[3]
            shot_team =  shot[4]
            key = '{}_{}_{}'.format(date, home_team, away_team)
            points =  int(shot[3])
            if shot_team == home_team:
                acummulated_score = AcummulatedScore(points, 0)
            else:
                acummulated_score = AcummulatedScore(0, points)
            games.update({key: acummulated_score})

        def get_summaries(games):
            for game in games:
                yield '{} {}'.format(game, str(games.get(game)))

        super(SumUpGames, self).__init__(incoming_address, 
                                            incoming_port,
                                            outgoing_address,
                                            outgoing_port,
                                            number_of_aggregator,
                                            init_state,
                                            update_state,
                                            get_summaries)
