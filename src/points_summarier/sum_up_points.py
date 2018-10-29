from multiprocessing import Process
from collections import Counter
import zmq

END_TOKEN = 'END'
class SumUpPoints(Process):

    def __init__(self, points_filter, incoming_address, incoming_port):
        self.incoming_address = incoming_address
        self.incoming_port = incoming_port   
        self.points_filter = points_filter
        super(SumUpPoints, self).__init__()

    def _init(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        self.socket.connect('tcp://{}:{}'.format(self.incoming_address, self.incoming_port))
      

    def _get_row(self):

        x = self.socket.recv_pyobj()

        return x


    def run(self):
        self._init()

        row = self._get_row()
        players_points = Counter()
        scored_shots = 0
        total_shots = 0

        while row != 'END':
            total_shots += 1 
            if row[0] == 'SCORED':
                scored_shots += 1
            row = self._get_row()

        print('% {}pts scored: {}'.format(self.points_filter, float(scored_shots) / total_shots))

        self._close()

    def _close(self):
        self.socket.close()
        self.context.term()



