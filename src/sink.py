
from multiprocessing import Process
from score import AcummulatedScore
import zmq
class Sink(Process):
    def __init__(self, incoming_address, incoming_port, name_file):
        self.incoming_address = incoming_address
        self.incoming_port = incoming_port
        self.name_file = name_file
        super(Sink, self).__init__()

    def _init(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        # We can connect to several endpoints if we desire, and receive from all.
        self.socket.bind('tcp://{}:{}'.format(self.incoming_address, self.incoming_port))

    def _get_result(self):
        return self.socket.recv_string()


    def run(self):
        self._init()
        
        result = self._get_result()

        with open(self.name_file, 'w') as output_file:
            while result != 'END':
                output_file.write(result)
                result = self._get_result()
                print(result)

        self._close()

    def _close(self):
        self.socket.close()
        self.context.term()