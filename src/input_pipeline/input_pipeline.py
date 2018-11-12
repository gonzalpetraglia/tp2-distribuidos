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
        self.number_filter_columns = 10
        self.number_readers = 10
        super(Input, self).__init__()


    def run(self):
        readers = []
        for i in range(self.number_readers):
            readers.append(Reader('127.0.0.1', self.range_port_init, i, self.number_readers))
        streamer = Streamer('127.0.0.1', self.range_port_init, '127.0.0.1', self.range_port_init + 1, self.number_readers, self.number_filter_columns)
        filters_columns = []
        for i in range(self.number_filter_columns):
            filters_columns.append(FilterColumns('127.0.0.1', self.range_port_init + 1, '127.0.0.1', self.range_port_init + 2))
        input_ventilator = StreamerPublisher('127.0.0.1', self.range_port_init + 2, self.outgoing_address, self.outgoing_port, 1)

        for reader in readers:
            reader.start()
        streamer.start()
        for filter_columns in filters_columns:
            filter_columns.start()
        
        input_ventilator.start()

        for reader in readers:
            reader.join()
        streamer.join()
        for filter_columns in filters_columns:
            filter_columns.join()
        input_ventilator.join()