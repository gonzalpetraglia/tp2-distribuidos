
from multiprocessing import Process
import zmq

END_TOKEN = 'END'
class Sink(Process):
    def __init__(self, incoming_address, incoming_port, name_file):
        self.incoming_address = incoming_address
        self.incoming_port = incoming_port
        self.name_file = name_file
        super(Sink, self).__init__()

    def _init(self):
        self.context = zmq.Context()
        self.frontend = self.context.socket(zmq.PULL)
        # We can connect to several endpoints if we desire, and receive from all.
        self.frontend.bind('tcp://{}:{}'.format(self.incoming_address, self.incoming_port))

    def _get_result(self):
        return self.frontend.recv_json()


    def run(self):
        self._init()
        
        result = self._get_result()

        with open(self.name_file, 'w') as output_file:
            while result != END_TOKEN:
                output_file.write(result)
                output_file.write('\n')
                result = self._get_result()

        self._close()

    def _close(self):
        from time import sleep
        sleep(20)
        
        self.frontend.close()
        self.context.term()