from multiprocessing import Process
from collections import Counter
import zmq
from .filter_columns import FilterColumns
from .filter_by_score import FilterByScore
from .sum_up_points import SumUpPoints
from streamer import Streamer


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
        sum_up_points = SumUpPoints(self.filter_points, '127.0.0.1', self.incoming_port + self.filter_points * 50 + 3)

        filter_columns.start()
        streamer_filtered_columns.start()
        filter_by_points.start()
        streamer_scored_goals.start()
        sum_up_points.start()

        filter_columns.join()
        streamer_filtered_columns.join()
        filter_by_points.join()
        streamer_scored_goals.join()
        sum_up_points.join()
