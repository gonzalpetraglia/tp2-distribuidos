from multiprocessing import Process
from collections import Counter
import zmq
from .filter_columns import FilterColumns
from .filter_scored import FilterScored
from .sum_up_games import SumUpGames
from zmq_streamer import Streamer


END_TOKEN = 'END'
class GamesCalculator(Process):

    def __init__(self, incoming_address, incoming_port, outgoing_address, outgoing_port):
        self.incoming_address = incoming_address
        self.incoming_port = incoming_port
        self.outgoing_address = outgoing_address
        self.outgoing_port = outgoing_port
        super(GamesCalculator, self).__init__()


    def run(self):
        # streamer that subscribes?
        filter_columns = FilterColumns(self.incoming_address, self.incoming_port, '127.0.0.1', 2010)
        #streamer_filtered_columns = Streamer(2010, 2011, '127.0.0.1', '127.0.0.1')
        filter_scored = FilterScored('127.0.0.1', 2010, '127.0.0.1', 2012)
        # streamer_scored_goals = Streamer(2012,2013, '127.0.0.1', '127.0.0.1')
        games_summer = SumUpGames('127.0.0.1', 2012, self.outgoing_address, self.outgoing_port)

        filter_columns.start()
        #streamer_filtered_columns.start()
        filter_scored.start()
        # streamer_scored_goals.start()
        games_summer.start()

        filter_columns.join()
        #streamer_filtered_columns.join()
        filter_scored.join()
        # streamer_scored_goals.join()
        games_summer.join()