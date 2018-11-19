
from ranking import Ranking, RankingCandidate
from stateful_processer_puller import StatefulProcesserPuller


class RankingMaker(StatefulProcesserPuller):
    def __init__(self, incoming_address, incoming_port, outgoing_address, outgoing_port):
        def init_state():
            return Ranking(10)
        
        def update_state(ranking, player):
            ranking.consider(RankingCandidate(player[0], player[1]))


        def get_summaries(ranking):
            yield str(ranking)

        super(RankingMaker, self).__init__(incoming_address, 
                                            incoming_port,
                                            outgoing_address,
                                            outgoing_port,
                                            init_state,
                                            update_state,
                                            get_summaries)



