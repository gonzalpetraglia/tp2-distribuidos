from collections import Counter
from multiprocessing import Process
import zmq

END_TOKEN = 'END'
class Numerator(Process):

    def __init__(self, incoming_address, incoming_port):
        self.incoming_address = incoming_address
        self.incoming_port = incoming_port
        super(Numerator, self).__init__()

    def _init(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://{}:{}".format(self.incoming_address, self.incoming_port))
        self.counter = Counter()

    def run(self):
        self._init()
        service_name = self.socket.recv_string()

        while service_name != END_TOKEN:
                
            current_number = self.counter.get(service_name) 
            current_number = current_number if current_number is not None else 0

            self.counter.update({service_name: 1})

            self.socket.send_string(str(current_number))
            service_name = self.socket.recv_string()

        self._close()

    def _close(self):
        self.socket.close()
        self.context.term()