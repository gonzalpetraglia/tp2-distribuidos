from multiprocessing import Process
from collections import Counter
import zmq
from .filter_columns import FilterColumns
from .filter_by_score import FilterByScore
from .sum_up_points import SumUpPoints
from streamer import Streamer
from sink import Sink

END_TOKEN = 'END'
class PointsSummarier(Process):

    def __init__(self, filter_points, incoming_address, incoming_port):
        self.incoming_address = incoming_address
        self.incoming_port = int(incoming_port)
        self.filter_points = filter_points
        super(PointsSummarier, self).__init__()


    def run(self):
        # streamer that subscribes? #TODO
        filter_columns = FilterColumns(self.incoming_address, #TODO Improve this
                                       self.incoming_port,
                                       '127.0.0.1',
                                       self.incoming_port + self.filter_points * 50 )
        streamer_filtered_columns = Streamer('127.0.0.1',  str(self.incoming_port + self.filter_points * 50), '127.0.0.1',  str(self.incoming_port + self.filter_points * 50 +1) )
        filter_by_points = FilterByScore(self.filter_points, '127.0.0.1',  str(self.incoming_port + self.filter_points * 50 + 1), '127.0.0.1',  str(self.incoming_port + self.filter_points * 50 + 2))
        streamer_scored_goals = Streamer('127.0.0.1',  self.incoming_port + self.filter_points * 50 + 2, '127.0.0.1', str( self.incoming_port + self.filter_points * 50 + 3))
        sum_up_points = SumUpPoints('127.0.0.1', self.incoming_port + self.filter_points * 50 + 3, '127.0.0.1', self.incoming_port + self.filter_points * 50 + 4)
        sink = Sink('127.0.0.1', self.incoming_port + self.filter_points * 50 + 4, '% {}pts'.format(self.filter_points))

        filter_columns.start()
        streamer_filtered_columns.start()
        filter_by_points.start()
        streamer_scored_goals.start()
        sum_up_points.start()
        sink.start()

        filter_columns.join()
        print(1)
        streamer_filtered_columns.join()
        print(1)
        filter_by_points.join()
        print(1)
        streamer_scored_goals.join()
        print(1)
        sum_up_points.join()
        print(1)
        sink.join()
