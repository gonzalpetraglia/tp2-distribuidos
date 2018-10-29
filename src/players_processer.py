import os
from multiprocessing import Process
import zmq
from ranking import Ranking, RankingCandidate
from collections import Counter

RANKING_LENGTH = os.environ.get('RANKING_LENGTH', 10)
class PlayersProcesser(Process):
    def __init__(self, incoming_address, incoming_port):
        self.incoming_address = incoming_address
        self.incoming_port = incoming_port
        super(PlayersProcesser, self).__init__()

    def _init(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        # We can connect to several endpoints if we desire, and receive from all.
        self.socket.connect('tcp://{}:{}'.format(self.incoming_address, self.incoming_port))

        self.socket.setsockopt_string(zmq.SUBSCRIBE, '')

    def _get_row(self):
        return self.socket.recv_pyobj()

    def run(self):
        self._init()
        
        row = self._get_row()
        l2 = []
        while row != 'END':
            l2.append([row['current shot outcome'],
                    row['points'],
                    row['shoot player']]) #send
            row = self._get_row()



        l3 = map(lambda x: x[1:], filter(lambda x: x[0] == 'SCORED', l2)) # filter column that is redundant #send

        players_points = Counter()
        for l in l3:
            player = l[1]
            points = int(l[0])
            players_points.update({player: points})


        ranking = Ranking(10)
        for player in players_points:
            ranking.consider(RankingCandidate(player, players_points.get(player)))

        print('Ranking: ' + str(ranking))

        self._close()

    def _close(self):
        self.socket.close()
        self.context.term()

