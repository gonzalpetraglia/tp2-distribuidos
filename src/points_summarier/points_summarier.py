from multiprocessing import Process
from collections import Counter
import zmq
from .filter_columns import FilterColumns
from .filter_by_score import FilterByScore
from .sum_up_points import SumUpPoints
from streamer import Streamer
from streamer_subscriber import StreamerSubscriber
from sink import Sink

class PointsSummarier(Process):

    def __init__(self, config, filter_points, incoming_address, incoming_port):
        self.incoming_address = incoming_address
        self.incoming_port = int(incoming_port)
        self.filter_points = filter_points
        self.config = config
        super(PointsSummarier, self).__init__()


    def run(self):

        address_used_internally = self.config['address_used_internally']
        range_port_init = self.config['internal_range_port']


        number_of_filters_columns = self.config['number_of_filters_columns']
        number_of_filters_by_score = self.config['number_of_filters_by_score']

        streamer_input = StreamerSubscriber(self.incoming_address, self.incoming_port, address_used_internally, range_port_init, 1, number_of_filters_columns)


        filters_columns = []        
        for i in range(number_of_filters_columns):
            filters_columns.append(FilterColumns(address_used_internally, range_port_init, address_used_internally, range_port_init + 1 ))

        streamer_filtered_columns = Streamer(address_used_internally,  range_port_init+ 1, address_used_internally, range_port_init + 2, number_of_filters_columns, number_of_filters_by_score )
        filters_by_score = []
        for i in range(number_of_filters_by_score):
            filters_by_score.append(FilterByScore(self.filter_points, address_used_internally,  range_port_init + 2, address_used_internally, range_port_init + 3))
        streamer_filtered_points = Streamer(address_used_internally,  range_port_init + 3, address_used_internally, range_port_init + 4, number_of_filters_by_score, 1)
        sum_up_points = SumUpPoints(address_used_internally, range_port_init + 4, address_used_internally, range_port_init + 5)
        sink = Sink(address_used_internally, range_port_init + 5, self.config['output_filename'])
        
        streamer_input.start()
        for filter_columns in filters_columns:
            filter_columns.start()
        streamer_filtered_columns.start()
        for filter_by_score in filters_by_score:
            filter_by_score.start()
        streamer_filtered_points.start()
        sum_up_points.start()
        sink.start()


        streamer_input.join()
        for filter_columns in filters_columns:
            filter_columns.join()
        streamer_filtered_columns.join()
        for filter_by_score in filters_by_score:
            filter_by_score.join()
        streamer_filtered_points.join()
        sum_up_points.join()
        sink.join()
