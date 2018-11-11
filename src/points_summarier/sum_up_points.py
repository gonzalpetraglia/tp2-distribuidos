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
        self.frontend = self.context.socket(zmq.PULL)
        self.frontend.connect('tcp://{}:{}'.format(self.incoming_address, self.incoming_port))
      
        self.backend = self.context.socket(zmq.PUSH)
        self.backend.connect('tcp://{}:{}'.format(self.outgoing_address, self.outgoing_port))
      

    def _get_row(self):

        x = self.frontend.recv_json()

        return x

    def _send_result(self, result):
        self.backend.send_string(result)

    def run(self):
        self._init()

        row = self._get_row()
        players_points = Counter()
        scored_shots = 0
        total_shots = 0

        while row != END_TOKEN:
            total_shots += 1 
            if row[0] == 'SCORED':
                scored_shots += 1
            row = self._get_row()
        if total_shots != 0:
            result = '{}%'.format(float(scored_shots) / total_shots * 100)
        else:
            result = 'undefined'
        self._send_result(result)
        self._send_result(END_TOKEN)
        print('Finished sum up points')


        self._close()

    def _close(self):
        from time import sleep
        sleep(60)
        
        self.frontend.close()
        self.backend.close()
        self.context.term()



