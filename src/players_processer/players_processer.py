from multiprocessing import Process
from collections import Counter
import zmq
from .filter_columns import FilterColumns
from .filter_scored import FilterScored
from .sum_up_player import SumUpPlayers
from .ranking_maker import RankingMaker
from streamer import Streamer
from streamer_subscriber import StreamerSubscriber
from sink import Sink


END_TOKEN = 'END'
NUMBER_OF_FILTER_SCORED = 10
NUMBER_OF_SUM_UP_PLAYERS = 1
NUMBER_OF_FILTERS_COLUMNS = 10
class PlayersProcesser(Process):

    def __init__(self, incoming_address, incoming_port, range_port_init):
        self.incoming_address = incoming_address
        self.incoming_port = incoming_port
        self.range_port_init = range_port_init
        super(PlayersProcesser, self).__init__()


    def run(self):
        streamer_input = StreamerSubscriber(self.incoming_address, self.incoming_port, '127.0.0.1', self.range_port_init, 1, NUMBER_OF_FILTERS_COLUMNS)

        filters_columns = []        
        for i in range(NUMBER_OF_FILTERS_COLUMNS):
            filters_columns.append(FilterColumns('127.0.0.1', self.range_port_init, '127.0.0.1', self.range_port_init + 1))
        streamer_filtered_columns = Streamer('127.0.0.1', self.range_port_init + 1, '127.0.0.1', self.range_port_init + 2, NUMBER_OF_FILTERS_COLUMNS, NUMBER_OF_FILTER_SCORED)
        
        filters_scored = []
        for i in range(NUMBER_OF_FILTER_SCORED):
            filters_scored.append(FilterScored('127.0.0.1', self.range_port_init + 2, '127.0.0.1', self.range_port_init + 3))
        streamer_scored_goals = Streamer('127.0.0.1', self.range_port_init + 3, '127.0.0.1', self.range_port_init + 4, NUMBER_OF_FILTER_SCORED, NUMBER_OF_SUM_UP_PLAYERS)
        
        # Add subscriber here
        players_summers = []
        for i in range(NUMBER_OF_SUM_UP_PLAYERS):
            players_summers.append(SumUpPlayers('127.0.0.1', self.range_port_init + 4, '127.0.0.1', self.range_port_init + 5))
        ranking_maker = RankingMaker('127.0.0.1', self.range_port_init + 5, '127.0.0.1', self.range_port_init + 6)
        
        sink = Sink('127.0.0.1', self.range_port_init + 6, 'ranking-players.txt')
        
        streamer_input.start()
        for filter_columns in filters_columns:
            filter_columns.start()
        streamer_filtered_columns.start()
        for filter_scored in filters_scored:
            filter_scored.start()
        streamer_scored_goals.start()
        for players_summer in players_summers:
            players_summer.start()
        ranking_maker.start()
        sink.start()


        streamer_input.join()

        for filter_columns in filters_columns:    
            filter_columns.join()
        streamer_filtered_columns.join()
        for filter_scored in filters_scored:
            filter_scored.join()
        streamer_scored_goals.join()
        for player_summer in players_summers:
            players_summer.join()
        ranking_maker.join()
        sink.join()
