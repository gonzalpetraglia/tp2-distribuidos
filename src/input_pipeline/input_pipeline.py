from multiprocessing import Process
from collections import Counter
import zmq
from .reader import Reader
from .streamer_publisher import StreamerPublisher

END_TOKEN = 'END'

class Input(Process):

    def __init__(self, outgoing_address, outgoing_port, range_port_init):
        self.outgoing_address = outgoing_address
        self.outgoing_port = outgoing_port
        self.range_port_init = range_port_init
        super(Input, self).__init__()


    def run(self):

        reader = Reader('127.0.0.1', self.range_port_init)
        input_ventilator = StreamerPublisher('127.0.0.1', self.range_port_init, self.outgoing_address, self.outgoing_port, 1)

        reader.start()
        input_ventilator.start()

        reader.join()
        input_ventilator.join()