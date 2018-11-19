from multiprocessing import Process
from collections import Counter
import zmq
from .filter_columns import FilterColumns
from .filter_scored import FilterScored
from .sum_up_games import SumUpGames
from streamer import Streamer
from streamer_subscriber import StreamerSubscriber
from streamer_publisher import StreamerPublisher
from sink_subscriber import SinkSubscriber

NUMBER_OF_FILTER_SCORED = 10
NUMBER_OF_GAME_SUMMERS = 10
NUMBER_OF_SINK_FORWARDERS = 10
NUMBER_OF_OUTPUT_FORWARDERS = 10
NUMBER_OF_FILTERS_COLUMNS = 10
class GamesCalculator(Process):

    def __init__(self, incoming_address, incoming_port, outgoing_address, outgoing_port, range_port_init):
        self.incoming_address = incoming_address
        self.incoming_port = incoming_port
        self.outgoing_address = outgoing_address
        self.outgoing_port = outgoing_port
        self.range_port_init = range_port_init
        super(GamesCalculator, self).__init__()


    def run(self):
        streamer_input = StreamerSubscriber(self.incoming_address, self.incoming_port, '127.0.0.1', self.range_port_init, 1, NUMBER_OF_FILTERS_COLUMNS)

        filters_columns = []        
        for i in range(NUMBER_OF_FILTER_SCORED):
            filters_columns.append(FilterColumns('127.0.0.1', self.range_port_init, '127.0.0.1', self.range_port_init + 1))
        
        streamer_filtered_columns = Streamer('127.0.0.1', self.range_port_init + 1 , '127.0.0.1', self.range_port_init + 2, NUMBER_OF_FILTER_SCORED, NUMBER_OF_FILTER_SCORED)
        
        filters_scored = []
        for i in range(NUMBER_OF_FILTER_SCORED):
            filters_scored.append(FilterScored('127.0.0.1', self.range_port_init + 2, '127.0.0.1', self.range_port_init + 3 ))
        
        streamer_scored_goals = StreamerPublisher('127.0.0.1', self.range_port_init + 3 , '127.0.0.1', self.range_port_init + 4, NUMBER_OF_FILTER_SCORED, NUMBER_OF_GAME_SUMMERS,
                                lambda x: '{}_{}_{}'.format(x[0], x[1], x[2]))
        
        # Add subscriber here
        games_summers = []
        for i in range(NUMBER_OF_GAME_SUMMERS):
            games_summers.append(SumUpGames('127.0.0.1', self.range_port_init + 4, '127.0.0.1', self.range_port_init + 5, i))
        
        streamer_games = StreamerPublisher('127.0.0.1', self.range_port_init + 5, self.outgoing_address, self.outgoing_port, NUMBER_OF_GAME_SUMMERS)

        sink = SinkSubscriber(self.outgoing_address, self.outgoing_port,  'games.txt')

        streamer_input.start()
        for filter_columns in filters_columns:
            filter_columns.start()
        streamer_filtered_columns.start()
        for filter_scored in filters_scored:
            filter_scored.start()
        streamer_scored_goals.start()
        for games_summer in games_summers:    
            games_summer.start()
        streamer_games.start()
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
        streamer_games.join()
        sink.join()
