from multiprocessing import Process
from collections import Counter
import zmq
from .filter_columns import FilterColumns
from .filter_scored import FilterScored
from .sum_up_player import SumUpPlayers
from .ranking_maker import RankingMaker
from zmq_streamer import Streamer


END_TOKEN = 'END'
class PlayersProcesser(Process):

    def __init__(self, incoming_address, incoming_port):
        self.incoming_address = incoming_address
        self.incoming_port = incoming_port
        # self.outgoing_address = outgoing_address
        # self.outgoing_port = outgoing_port
        super(PlayersProcesser, self).__init__()


    def run(self):
        # streamer that subscribes?
        filter_columns = FilterColumns(self.incoming_address, self.incoming_port, '127.0.0.1', 2020)
        #streamer_filtered_columns = Streamer(2020, 2021, '127.0.0.1', '127.0.0.1')
        filter_scored = FilterScored('127.0.0.1', 2020, '127.0.0.1', 2022)
        # streamer_scored_goals = Streamer(2022,2023, '127.0.0.1', '127.0.0.1')
        players_summer = SumUpPlayers('127.0.0.1', 2022, '127.0.0.1', 2023)
        ranking_maker = RankingMaker('127.0.0.1', 2023)

        print('aaaa')
        filter_columns.start()
        print('aaaa')
        #streamer_filtered_columns.start()
        filter_scored.start()
        print('aaaa')
        # streamer_scored_goals.start()
        players_summer.start()

        print('aaaa')
        ranking_maker.start()


        print('aaaa')
        filter_columns.join()
        print('aaaa')
        #streamer_filtered_columns.join()
        filter_scored.join()
        print('aaaa')
        # streamer_scored_goals.join()
        players_summer.join()
        print('aaaa')
        ranking_maker.join()
        print('aaaa')