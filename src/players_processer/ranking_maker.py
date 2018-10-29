import os
from multiprocessing import Process
import zmq
from ranking import Ranking, RankingCandidate
from collections import Counter

RANKING_LENGTH = os.environ.get('RANKING_LENGTH', 10)
class RankingMaker(Process):
    def __init__(self, incoming_address, incoming_port):
        self.incoming_address = incoming_address
        self.incoming_port = incoming_port
        # self.outgoing_address = outgoing_address
        # self.outgoing_port = outgoing_port        
        super(RankingMaker, self).__init__()

    def _init(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        self.socket.connect('tcp://{}:{}'.format(self.incoming_address, self.incoming_port))


    def _get_row(self):
        x = self.socket.recv_pyobj()
        print('Ranking got '+ str(x))
        return x

    def run(self):
        self._init()
        ranking = Ranking(10)
 
        row = self._get_row()
        while row != 'END':
            ranking.consider(RankingCandidate(row[0], row[1]))
            row = self._get_row()

        print('Ranking: ' + str(ranking))


        self._close()



    def _close(self):
        self.socket.close()
        self.context.term()


