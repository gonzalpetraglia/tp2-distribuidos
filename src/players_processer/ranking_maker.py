import os
from multiprocessing import Process
import zmq
from ranking import Ranking, RankingCandidate
from collections import Counter

RANKING_LENGTH = os.environ.get('RANKING_LENGTH', 10)
END_TOKEN = 'END'
class RankingMaker(Process):
    def __init__(self, incoming_address, incoming_port, outgoing_address, outgoing_port):
        self.incoming_address = incoming_address
        self.incoming_port = incoming_port
        self.outgoing_address = outgoing_address
        self.outgoing_port = outgoing_port   
        super(RankingMaker, self).__init__()

    def _init(self):
        self.context = zmq.Context()
        self.frontend = self.context.socket(zmq.PULL)
        self.frontend.bind('tcp://{}:{}'.format(self.incoming_address, self.incoming_port))
      
        self.backend = self.context.socket(zmq.PUSH)
        self.backend.connect('tcp://{}:{}'.format(self.outgoing_address, self.outgoing_port))
      

    def _get_row(self):
        x = self.frontend.recv_json()
        return x

    def _send_result(self, message):
        self.backend.send_string(message)

    def run(self):
        self._init()
        ranking = Ranking(10)
 
        row = self._get_row()
        while row != END_TOKEN:
            ranking.consider(RankingCandidate(row[0], row[1]))
            row = self._get_row()

        # for place in ranking:
        #     result = str(place)
        #     self._send_result(result)

        self._send_result(str(ranking))
        self._send_result(END_TOKEN)
        self._close()



    def _close(self):
        from time import sleep
        sleep(20)
        
        self.frontend.close()
        self.backend.close()
        self.context.term()


