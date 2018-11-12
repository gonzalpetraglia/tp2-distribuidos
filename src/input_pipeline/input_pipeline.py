from multiprocessing import Process
from collections import Counter
import zmq
from .reader import Reader
from .streamer_publisher import StreamerPublisher
from .filter_columns import FilterColumns
from streamer import Streamer


class Input(Process):

    def __init__(self, outgoing_address, outgoing_port, range_port_init):
        self.outgoing_address = outgoing_address
        self.outgoing_port = outgoing_port
        self.range_port_init = range_port_init
        super(Input, self).__init__()


    def run(self):

        reader = Reader('127.0.0.1', self.range_port_init)
        streamer = Streamer('127.0.0.1', self.range_port_init, '127.0.0.1', self.range_port_init + 1, 1, 1)
        filter_columns = FilterColumns('127.0.0.1', self.range_port_init + 1, '127.0.0.1', self.range_port_init + 2)
        input_ventilator = StreamerPublisher('127.0.0.1', self.range_port_init + 2, self.outgoing_address, self.outgoing_port, 1)


        reader.start()
        streamer.start()
        filter_columns.start()
        input_ventilator.start()

        reader.join()
        streamer.join()
        filter_columns.join()
        input_ventilator.join()