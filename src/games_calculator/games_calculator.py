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

class GamesCalculator(Process):

    def __init__(self, config, incoming_address, incoming_port, outgoing_address, outgoing_port, numerator_address, numerator_port):
        self.incoming_address = incoming_address
        self.incoming_port = incoming_port
        self.outgoing_address = outgoing_address
        self.outgoing_port = outgoing_port
        self.config = config
        self.numerator_address = numerator_address 
        self.numerator_port = numerator_port
        super(GamesCalculator, self).__init__()


    def run(self):
        address_used_internally = self.config['address_used_internally']
        range_port_init = self.config['internal_range_port']
                
        number_of_filter_scored = self.config['number_of_filter_scored']
        number_of_game_summers = self.config['number_of_game_summers']
        number_of_filters_columns = self.config['number_of_filters_columns']

        streamer_input = StreamerSubscriber(self.incoming_address, self.incoming_port, address_used_internally, range_port_init, 1, number_of_filters_columns)

        filters_columns = []        
        for i in range(number_of_filter_scored):
            filters_columns.append(FilterColumns(address_used_internally, range_port_init, address_used_internally, range_port_init + 1))
        
        streamer_filtered_columns = Streamer(address_used_internally, range_port_init + 1 , address_used_internally, range_port_init + 2, number_of_filters_columns, number_of_filter_scored)
        
        filters_scored = []
        for i in range(number_of_filters_columns):
            filters_scored.append(FilterScored(address_used_internally, range_port_init + 2, address_used_internally, range_port_init + 3 ))
        
        streamer_scored_goals = StreamerPublisher(address_used_internally, range_port_init + 3 , address_used_internally, range_port_init + 4, number_of_filter_scored, number_of_game_summers,
                                lambda x: '{}_{}_{}'.format(x[0], x[1], x[2]))
        
        # Add subscriber here
        games_summers = []
        for i in range(number_of_game_summers):
            games_summers.append(SumUpGames(address_used_internally, range_port_init + 4, address_used_internally, range_port_init + 5, self.numerator_address, self.numerator_port))
        
        streamer_games = StreamerPublisher(address_used_internally, range_port_init + 5, self.outgoing_address, self.outgoing_port, number_of_game_summers)

        sink = SinkSubscriber(self.outgoing_address, self.outgoing_port, self.config['output_filename'])

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
