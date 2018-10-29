from games_calculator.games_calculator import GamesCalculator
from games_summarier import GamesSummarier
from players_processer import PlayersProcesser
from points_summarier import PointsSummarier
from reader import Reader
from time import sleep

if __name__ == '__main__':
    incoming_address, incoming_port = '127.0.0.1', '2000'
    games_calculator = GamesCalculator(incoming_address, incoming_port, '127.0.0.1', '2001')
    games_summarier = GamesSummarier('127.0.0.1', '2001')
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

    sleep(1)
    reader.start()


    print('Wait reader')
    reader.join()
    print('Wait games calculator')
    games_calculator.join()
    print('Wait games summarier')
    games_summarier.join()

    print('Wait players processers')
    players_processer.join()

    print('Wait points summarier 3')
    points_summarier3.join()

    print('Wait games summarier 2')
    points_summarier2.join()





