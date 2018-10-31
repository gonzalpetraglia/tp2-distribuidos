from multiprocessing import Process
from collections import Counter
import zmq
from .filter_columns import FilterColumns
from .filter_scored import FilterScored
from .sum_up_player import SumUpPlayers
from .ranking_maker import RankingMaker
from streamer import Streamer
from sink import Sink


END_TOKEN = 'END'
NUMBER_OF_FILTER_SCORED = 10
NUMBER_OF_SUM_UP_PLAYERS = 1
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
        streamer_filtered_columns = Streamer('127.0.0.1', 2020, '127.0.0.1', 2021, 1, NUMBER_OF_FILTER_SCORED)
        filters_scored = []
        for i in range(NUMBER_OF_FILTER_SCORED):
            filters_scored.append(FilterScored('127.0.0.1', 2021, '127.0.0.1', 2022))
        streamer_scored_goals = Streamer('127.0.0.1', 2022, '127.0.0.1', 2023, NUMBER_OF_FILTER_SCORED, NUMBER_OF_SUM_UP_PLAYERS)
        players_summers = []
        for i in range(NUMBER_OF_SUM_UP_PLAYERS):
            players_summers.append(SumUpPlayers('127.0.0.1', 2023, '127.0.0.1', 2024))
        ranking_maker = RankingMaker('127.0.0.1', 2024, '127.0.0.1', 2025)
        sink = Sink('127.0.0.1', 2025, 'ranking-players.txt')

        filter_columns.start()
        streamer_filtered_columns.start()
        for filter_scored in filters_scored:
            filter_scored.start()
        streamer_scored_goals.start()
        for players_summer in players_summers:
            players_summer.start()
        ranking_maker.start()
        sink.start()



        filter_columns.join()
        streamer_filtered_columns.join()
        for filter_scored in filters_scored:
            filter_scored.join()
        streamer_scored_goals.join()
        for player_summer in players_summers:
            players_summer.join()
        ranking_maker.join()
        sink.join()
