from  multiprocessing import Process
import zmq

END_TOKEN = 'END'

class Source(Process):
    def _send_row(self, row):
        self.frontend.send_json(row)

    def __init__(self, incoming_address, incoming_port, lines):
        self.incoming_address = incoming_address
        self.incoming_port = incoming_port
        self._lines = lines
        super(Source, self).__init__()

    def _init(self):
        self.context = zmq.Context()
        self.frontend = self.context.socket(zmq.PUSH)
        self.frontend.connect('tcp://{}:{}'.format(self.incoming_address, self.incoming_port))
        
    def run(self):
        self._init()
        
        for line in self._lines():
            self._send_row(line)

        self._send_row(END_TOKEN)
        
        self._close()

    def _close(self):
        from time import sleep
        sleep(20)
        
        self.frontend.close()
        self.context.term()

