from multiprocessing import Process
import zmq
import json

END_TOKEN = 'END'
class StatefulProcesser(Process):

    def __init__(self, incoming_address, incoming_port, outgoing_address, outgoing_port, numerator_address, numerator_port, service_name, init_state, update_state, get_summaries):
        self.incoming_address = incoming_address
        self.incoming_port = incoming_port
        self.outgoing_address = outgoing_address
        self.outgoing_port = outgoing_port        
        self.numerator_address = numerator_address
        self.numerator_port = numerator_port
        self.service_name = service_name
        self._init_state = init_state
        self._update_state = update_state
        self._get_summaries = get_summaries
        super(StatefulProcesser, self).__init__()

    def _init(self):
        self.context = zmq.Context()

        numerator_socket = self.context.socket(zmq.REQ)
        numerator_socket.connect("tcp://{}:{}".format(self.numerator_address, self.numerator_port))
        numerator_socket.send_string(self.service_name)

        self.number_of_aggregator = numerator_socket.recv_string()


        self.frontend = self.context.socket(zmq.SUB)
        self.frontend.connect('tcp://{}:{}'.format(self.incoming_address, self.incoming_port))
        self.frontend.setsockopt_string(zmq.SUBSCRIBE, str(self.number_of_aggregator))

        self.backend = self.context.socket(zmq.PUSH)
        self.backend.connect('tcp://{}:{}'.format(self.outgoing_address, self.outgoing_port))
        

    def _get_input(self):

        _, msg = self.frontend.recv_multipart()
        msg = msg.decode()
        if msg != END_TOKEN:
            msg = json.loads(msg)
        return msg

    def _send_summary(self, summary):
        self.backend.send_json(summary)

    def run(self):
        self._init()

        input_line = self._get_input()


        state = self._init_state()
        while input_line != END_TOKEN:

            
            self._update_state(state, input_line)
            input_line = self._get_input()
            

        for summary in self._get_summaries(state):
            self._send_summary(summary) 

        self._send_summary(END_TOKEN)
        self._close()

    def _close(self):
        from time import sleep
        sleep(20)
        
        self.frontend.close()
        self.backend.close()
        self.context.term()



