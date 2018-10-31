from multiprocessing import Process
from collections import Counter
import zmq

END_TOKEN = 'END'
class SumUpPoints(Process):

    def __init__(self, incoming_address, incoming_port, outgoing_address, outgoing_port):
        self.incoming_address = incoming_address
        self.incoming_port = incoming_port
        self.outgoing_address = outgoing_address
        self.outgoing_port = outgoing_port   
        super(SumUpPoints, self).__init__()

    def _init(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        self.socket.connect('tcp://{}:{}'.format(self.incoming_address, self.incoming_port))
      
        self.socket2 = self.context.socket(zmq.PUSH)
        self.socket2.connect('tcp://{}:{}'.format(self.outgoing_address, self.outgoing_port))
      

    def _get_row(self):

        x = self.socket.recv_pyobj()

        return x

    def _send_result(self, result):
        self.socket2.send_string(result)

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

        result = '{}%'.format(float(scored_shots) / total_shots * 100)

        self._send_result(result)
        self._send_result('END')

        self._close()

    def _close(self):
        from time import sleep
        sleep(20)
        
        self.socket.close()
        self.socket2.close()
        self.context.term()



