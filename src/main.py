from games_calculator.games_calculator import GamesCalculator
from games_summarier.games_summarier_pipeline import GamesSummarierPipeline
from players_processer.players_processer import PlayersProcesser
from points_summarier.points_summarier import PointsSummarier
from input_pipeline.input_pipeline import Input
from sink import Sink

if __name__ == '__main__':

    input_address, input_port = '127.0.0.1', 2000
    games_summarier_address, games_summarier_port = '127.0.0.1', 2001
    input_pipe = Input(input_address, input_port, 2500)
    games_calculator = GamesCalculator(input_address, input_port, games_summarier_address, games_summarier_port, 2400)
    games_summarier = GamesSummarierPipeline(games_summarier_address, games_summarier_port, 2600)
    players_processer = PlayersProcesser(input_address, input_port, 2100)
    points_summarier2 = PointsSummarier(2, input_address, input_port, 2200)
    points_summarier3 = PointsSummarier(3, input_address, input_port, 2300)


    print ('Started')
    games_calculator.start()
    games_summarier.start()
    players_processer.start()
    points_summarier3.start()
    points_summarier2.start()
    input_pipe.start()


    games_calculator.join()
    games_summarier.join()
    players_processer.join()
    points_summarier3.join()
    points_summarier2.join()
    input_pipe.join()




