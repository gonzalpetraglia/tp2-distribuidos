from games_calculator.games_calculator import GamesCalculator
from games_summarier.games_summarier_pipeline import GamesSummarierPipeline
from players_processer.players_processer import PlayersProcesser
from points_summarier.points_summarier import PointsSummarier
from input_pipeline.input_pipeline import Input
from numerator import Numerator
import json

END_TOKEN = 'END'
if __name__ == '__main__':
    with open('src/config.json') as config_json:
        config = json.load(config_json)
    numerator_address, numerator_port = config['numerator_address'], config['numerator_port']
    input_address, input_port = config['input_address'], config['input_port']
    games_summarier_address, games_summarier_port = config['game_summarier_address'], config['game_summarier_port']


    input_pipe = Input(config['input_pipe'], input_address, input_port)
    games_calculator = GamesCalculator(config['games_calculator'], input_address, input_port, games_summarier_address, games_summarier_port, numerator_address, numerator_port)
    games_summarier = GamesSummarierPipeline(config['games_summarier'], games_summarier_address, games_summarier_port)
    players_processer = PlayersProcesser(config['players_processer'], input_address, input_port, numerator_address, numerator_port)
    points_summarier2 = PointsSummarier(config['points_summarier2'], 2, input_address, input_port)
    points_summarier3 = PointsSummarier(config['points_summarier3'], 3, input_address, input_port)
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
