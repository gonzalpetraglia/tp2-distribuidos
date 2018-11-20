from multiprocessing import Process
from collections import Counter
import zmq
from .reader import Reader
from streamer_publisher import StreamerPublisher
from .filter_columns import FilterColumns
from streamer import Streamer


class Input(Process):

    def __init__(self, config, outgoing_address, outgoing_port):
        self.outgoing_address = outgoing_address
        self.outgoing_port = outgoing_port
        self.config = config
        super(Input, self).__init__()


    def run(self):
        address_used_internally = self.config['address_used_internally']
        range_port_init = self.config['internal_range_port']
        number_filter_columns = self.config['number_filter_columns']
        number_readers = self.config['number_readers']

        readers = []
        for i in range(number_readers):
            readers.append(Reader(self.config['reader'], address_used_internally, range_port_init, i, number_readers))
        
        streamer = Streamer(address_used_internally, range_port_init, address_used_internally, range_port_init + 1, number_readers, number_filter_columns)
        
        filters_columns = []
        for i in range(number_filter_columns):
            filters_columns.append(FilterColumns(address_used_internally, range_port_init + 1, address_used_internally, range_port_init + 2))
        
        input_ventilator = StreamerPublisher(address_used_internally, range_port_init + 2, self.outgoing_address, self.outgoing_port, number_filter_columns)

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