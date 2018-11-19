from multiprocessing import Process
import zmq

END_TOKEN = 'END'
class StatelessProcesser(Process):

    def __init__(self, incoming_address, incoming_port, outgoing_address, outgoing_port, process_input):
        self.incoming_address = incoming_address
        self.incoming_port = incoming_port
        self.outgoing_address = outgoing_address
        self.outgoing_port = outgoing_port  
        self._process_input = process_input      
        super(StatelessProcesser, self).__init__()

    def _init(self):
        self.context = zmq.Context()
        self.frontend = self.context.socket(zmq.PULL)
        self.frontend.connect('tcp://{}:{}'.format(self.incoming_address, self.incoming_port))
        
        self.backend = self.context.socket(zmq.PUSH)
        self.backend.connect('tcp://{}:{}'.format(self.outgoing_address, self.outgoing_port))
        
    def _get_input(self):
        return self.frontend.recv_json()

    def _send_result(self, columns):
        self.backend.send_json(columns)

    def run(self):
        self._init()
        input_line = self._get_input()

        while input_line != END_TOKEN:
            result = self._process_input(input_line)
            if result is not None:
                self._send_result(result)

            input_line = self._get_input()

        self._send_result(END_TOKEN)
        self._close()

    def _close(self):
        from time import sleep
        sleep(20)
        
        self.frontend.close()
        self.backend.close()
        self.context.term()
