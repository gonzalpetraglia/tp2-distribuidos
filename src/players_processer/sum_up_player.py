from collections import Counter
from stateful_processer import StatefulProcesser


class SumUpPlayers(StatefulProcesser):
    def __init__(self, incoming_address, incoming_port, outgoing_address, outgoing_port, numerator_address, numerator_port):
        def init_state():
            return Counter()
        
        def update_state(players_points, shoot):

            player = shoot[1]
            points = int(shoot[0])
            players_points.update({player: points})

        def get_summaries(players_points):
            for player_points in players_points:
                yield [player_points, players_points.get(player_points)]

        super(SumUpPlayers, self).__init__(incoming_address, 
                                            incoming_port,
                                            outgoing_address,
                                            outgoing_port,
                                            numerator_address,
                                            numerator_port,
                                            'sum_up_players',
                                            init_state,
                                            update_state,
                                            get_summaries)
