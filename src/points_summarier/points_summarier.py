from multiprocessing import Process
from collections import Counter
import zmq
from .filter_columns import FilterColumns
from .filter_by_score import FilterByScore
from .sum_up_points import SumUpPoints
from streamer import Streamer
from streamer_subscriber import StreamerSubscriber
from sink import Sink

NUMBER_OF_FILTERS_COLUMNS = 10
NUMBER_OF_FILTERS_BY_SCORE = 10
class PointsSummarier(Process):

    def __init__(self, filter_points, incoming_address, incoming_port, range_port_init):
        self.incoming_address = incoming_address
        self.incoming_port = int(incoming_port)
        self.filter_points = filter_points
        self.range_port_init = range_port_init
        super(PointsSummarier, self).__init__()


    def run(self):
        streamer_input = StreamerSubscriber(self.incoming_address, self.incoming_port, '127.0.0.1', self.range_port_init, 1, NUMBER_OF_FILTERS_COLUMNS)


        filters_columns = []        
        for i in range(NUMBER_OF_FILTERS_COLUMNS):
            filters_columns.append(FilterColumns('127.0.0.1', self.range_port_init, '127.0.0.1', self.range_port_init + 1 ))

        streamer_filtered_columns = Streamer('127.0.0.1',  self.range_port_init+ 1, '127.0.0.1', self.range_port_init + 2, NUMBER_OF_FILTERS_COLUMNS, NUMBER_OF_FILTERS_BY_SCORE )
        filters_by_score = []
        for i in range(NUMBER_OF_FILTERS_BY_SCORE):
            filters_by_score.append(FilterByScore(self.filter_points, '127.0.0.1',  self.range_port_init + 2, '127.0.0.1', self.range_port_init + 3))
        streamer_scored_goals = Streamer('127.0.0.1',  self.range_port_init + 3, '127.0.0.1', self.range_port_init + 4, NUMBER_OF_FILTERS_BY_SCORE, 1)
        sum_up_points = SumUpPoints('127.0.0.1', self.range_port_init + 4, '127.0.0.1', self.range_port_init + 5)
        sink = Sink('127.0.0.1', self.range_port_init + 5, '%-{}pts.txt'.format(self.filter_points))

        streamer_input.start()
        for filter_columns in filters_columns:
            filter_columns.start()
        streamer_filtered_columns.start()
        for filter_by_score in filters_by_score:
            filter_by_score.start()
        streamer_scored_goals.start()
        sum_up_points.start()
        sink.start()


        streamer_input.join()
        for filter_columns in filters_columns:

            filter_columns.join()
        streamer_filtered_columns.join()
        for filter_by_score in filters_by_score:
            filter_by_score.join()
        streamer_scored_goals.join()
        sum_up_points.join()
        sink.join()
