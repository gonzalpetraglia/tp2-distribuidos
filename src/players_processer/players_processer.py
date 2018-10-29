from multiprocessing import Process
from collections import Counter
import zmq
from .filter_columns import FilterColumns
from .filter_scored import FilterScored
from .sum_up_player import SumUpPlayers
from .ranking_maker import RankingMaker
from streamer import Streamer


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
        streamer_filtered_columns = Streamer('127.0.0.1', 2020, '127.0.0.1', 2021)
        filter_scored = FilterScored('127.0.0.1', 2021, '127.0.0.1', 2022)
        streamer_scored_goals = Streamer('127.0.0.1', 2022, '127.0.0.1', 2023)
        players_summer = SumUpPlayers('127.0.0.1', 2023, '127.0.0.1', 2024)
        ranking_maker = RankingMaker('127.0.0.1', 2024)

        filter_columns.start()
        streamer_filtered_columns.start()
        filter_scored.start()
        streamer_scored_goals.start()
        players_summer.start()
        ranking_maker.start()



        filter_columns.join()
        streamer_filtered_columns.join()
        filter_scored.join()
        streamer_scored_goals.join()
        players_summer.join()
        ranking_maker.join()
