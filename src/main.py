from games_calculator.games_calculator import GamesCalculator
from games_summarier.games_summarier_pipeline import GamesSummarierPipeline
from players_processer.players_processer import PlayersProcesser
from points_summarier.points_summarier import PointsSummarier
from input_pipeline.input_pipeline import Input
from numerator import Numerator

END_TOKEN = 'END'
if __name__ == '__main__':

    numerator_address, numerator_port = '127.0.0.1', 5557
    input_address, input_port = '127.0.0.1', 2000
    games_summarier_address, games_summarier_port = '127.0.0.1', 2001


    input_pipe = Input(input_address, input_port, 2500)
    games_calculator = GamesCalculator(input_address, input_port, games_summarier_address, games_summarier_port, 2400, numerator_address, numerator_port)
    games_summarier = GamesSummarierPipeline(games_summarier_address, games_summarier_port, 2600)
    players_processer = PlayersProcesser(input_address, input_port, 2100, numerator_address, numerator_port)
    points_summarier2 = PointsSummarier(2, input_address, input_port, 2200)
    points_summarier3 = PointsSummarier(3, input_address, input_port, 2300)
    numerator = Numerator(numerator_address, numerator_port)


    print ('Starting')
    input_pipe.start()
    games_calculator.start()
    games_summarier.start()
    players_processer.start()
    points_summarier3.start()
    points_summarier2.start()
    numerator.start()

    input_pipe.join()
    games_calculator.join()
    games_summarier.join()
    players_processer.join()
    points_summarier2.join()
    points_summarier3.join()

    import zmq
    context = zmq.Context()

    socket = context.socket(zmq.REQ)
    socket.connect("tcp://{}:{}".format(numerator_address, numerator_port))

    socket.send_string(END_TOKEN)

    numerator.join()
