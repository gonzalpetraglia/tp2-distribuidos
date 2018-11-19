from stateful_processer_puller import StatefulProcesserPuller
from score import AcummulatedScore

class GamesSummarier(StatefulProcesserPuller):
    def __init__(self, incoming_address, incoming_port, outgoing_address, outgoing_port):
        def init_state():
            return {"home wins": 0, "total games": 0}
        
        def update_state(accumulator, game_string):
            score_string = game_string.split(" ")[1]
            score = AcummulatedScore.from_string(score_string)

            accumulator["total games"] += 1 
            if score.home_wins():
                accumulator["home wins"] += 1

        def get_summaries(accumulator):
            home_wins = accumulator["home wins"]
            total_games = accumulator["total games"]
            yield "{}%".format(float(home_wins) / total_games * 100) if total_games else 'undefined'

        super(GamesSummarier, self).__init__(incoming_address, 
                                            incoming_port,
                                            outgoing_address,
                                            outgoing_port,
                                            init_state,
                                            update_state,
                                            get_summaries)



