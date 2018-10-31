from games_calculator.games_calculator import GamesCalculator
from games_summarier import GamesSummarier
from players_processer.players_processer import PlayersProcesser
from points_summarier.points_summarier import PointsSummarier
from reader import Reader
from sink import Sink

if __name__ == '__main__':
    incoming_address, incoming_port = '127.0.0.1', '2000'
    games_calculator = GamesCalculator(incoming_address, incoming_port, '127.0.0.1', '2001')
    games_summarier = GamesSummarier('127.0.0.1', '2001', '127.0.0.1', 2002)
    sink = Sink('127.0.0.1', 2002, '%home-wins.txt')
    players_processer = PlayersProcesser(incoming_address, incoming_port)
    points_summarier2 = PointsSummarier(2, incoming_address, incoming_port)
    points_summarier3 = PointsSummarier(3, incoming_address, incoming_port)
    reader = Reader(incoming_address, incoming_port)


    print ('Started')
    games_calculator.start()
    games_summarier.start()
    players_processer.start()
    points_summarier3.start()
    points_summarier2.start()
    sink.start()

    reader.start()


    reader.join()
    games_calculator.join()
    games_summarier.join()
    players_processer.join()
    points_summarier3.join()
    points_summarier2.join()
    sink.join()




