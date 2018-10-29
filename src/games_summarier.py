
from multiprocessing import Process
from score import AcummulatedScore
import zmq
class GamesSummarier(Process):
    def __init__(self, incoming_address, incoming_port):
        self.incoming_address = incoming_address
        self.incoming_port = incoming_port
        super(GamesSummarier, self).__init__()

    def _init(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        # We can connect to several endpoints if we desire, and receive from all.
        self.socket.connect('tcp://{}:{}'.format(self.incoming_address, self.incoming_port))

        self.socket.setsockopt_string(zmq.SUBSCRIBE, '')

    def _get_game(self):
        return self.socket.recv_pyobj()

    def run(self):
        self._init()
        
        home_wins = 0
        total_games = 0
        score = self._get_game()

        while score != 'END':
            
            total_games += 1 
            if score.home_wins():
                home_wins += 1
            
            score = self._get_game()


        print('% wins home team:' + str(float(home_wins) / total_games))

        self._close()

    def _close(self):
        self.socket.close()
        self.context.term()