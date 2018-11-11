from multiprocessing import Process
from collections import Counter
import zmq
from .filter_columns import FilterColumns
from .filter_scored import FilterScored
from .sum_up_games import SumUpGames
from streamer import Streamer
from streamer_subscriber import StreamerSubscriber
from sink import Sink

END_TOKEN = 'END'


NUMBER_OF_FILTER_SCORED = 10
NUMBER_OF_GAME_SUMMERS = 1
NUMBER_OF_FILTERS_COLUMNS = 10
class GamesCalculator(Process):

    def __init__(self, incoming_address, incoming_port, outgoing_address, outgoing_port):
        self.incoming_address = incoming_address
        self.incoming_port = incoming_port
        self.outgoing_address = outgoing_address
        self.outgoing_port = outgoing_port
        super(GamesCalculator, self).__init__()


    def run(self):
        streamer_input = StreamerSubscriber(self.incoming_address, self.incoming_port, '127.0.0.1', 2010, 1, NUMBER_OF_FILTERS_COLUMNS)

        filters_columns = []        
        for i in range(NUMBER_OF_FILTER_SCORED):
            filters_columns.append(FilterColumns('127.0.0.1', 2010, '127.0.0.1', 2011))
        
        streamer_filtered_columns = Streamer('127.0.0.1', 2011, '127.0.0.1', 2012, NUMBER_OF_FILTER_SCORED, NUMBER_OF_FILTER_SCORED)
        
        filters_scored = []
        for i in range(NUMBER_OF_FILTER_SCORED):
            filters_scored.append(FilterScored('127.0.0.1', 2012, '127.0.0.1', 2013))
        
        streamer_scored_goals = Streamer('127.0.0.1', 2013, '127.0.0.1', 2014, NUMBER_OF_FILTER_SCORED, NUMBER_OF_GAME_SUMMERS)
        
        games_summers = []
        for i in range(NUMBER_OF_GAME_SUMMERS):
            games_summers.append(SumUpGames('127.0.0.1', 2014, self.outgoing_address, self.outgoing_port, '127.0.0.1', 2015))
        
        sink = Sink('127.0.0.1', 2015, 'games.txt')


        streamer_input.start()
        for filter_columns in filters_columns:
            filter_columns.start()
        streamer_filtered_columns.start()
        for filter_scored in filters_scored:
            filter_scored.start()
        streamer_scored_goals.start()
        for games_summer in games_summers:    
            games_summer.start()
        sink.start()

        streamer_input.join()
        for filter_columns in filters_columns:
            filter_columns.join()
        streamer_filtered_columns.join()
        for filter_scored in filters_scored:
            filter_scored.join()
        streamer_scored_goals.join()
        for games_summer in games_summers:    
            games_summer.join()
        sink.join()