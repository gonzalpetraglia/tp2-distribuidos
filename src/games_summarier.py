
from multiprocessing import Process
from score import AcummulatedScore
import zmq
class GamesSummarier(Process):
    def __init__(self, incoming_address, incoming_port, outcoming_address, outcoming_port):
        self.incoming_address = incoming_address
        self.incoming_port = incoming_port
        self.outcoming_address = outcoming_address
        self.outcoming_port = outcoming_port
        super(GamesSummarier, self).__init__()

    def _init(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        # We can connect to several endpoints if we desire, and receive from all.
        self.socket.connect('tcp://{}:{}'.format(self.incoming_address, self.incoming_port))
        
        self.socket2 = self.context.socket(zmq.PUSH)
        # We can connect to several endpoints if we desire, and receive from all.
        self.socket2.connect('tcp://{}:{}'.format(self.outcoming_address, self.outcoming_port))

    def _get_game(self):
        return self.socket.recv_string()

    def _send_result(self, result):
        self.socket2.send_string(result)

    def run(self):
        self._init()
        
        home_wins = 0
        total_games = 0
        score_string = self._get_game()

        while score_string != 'END':
            score = AcummulatedScore.from_string(score_string)

            
            total_games += 1 
            if score.home_wins():
                home_wins += 1
            
            score_string = self._get_game()

        self._send_result("{}%".format(float(home_wins) / total_games * 100 ))
        self._send_result("END")
        self._close()

    def _close(self):
        self.socket.close()
        self.socket2.close()
        self.context.term()