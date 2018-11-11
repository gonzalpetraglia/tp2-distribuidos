
from multiprocessing import Process
from score import AcummulatedScore
import zmq

END_TOKEN = 'END'

class GamesSummarier(Process):
    def __init__(self, incoming_address, incoming_port, outcoming_address, outcoming_port):
        self.incoming_address = incoming_address
        self.incoming_port = incoming_port
        self.outcoming_address = outcoming_address
        self.outcoming_port = outcoming_port
        super(GamesSummarier, self).__init__()

    def _init(self):
        self.context = zmq.Context()
        self.frontend = self.context.socket(zmq.PULL)
        # We can connect to several endpoints if we desire, and receive from all.
        self.frontend.connect('tcp://{}:{}'.format(self.incoming_address, self.incoming_port))
        
        self.backend = self.context.socket(zmq.PUSH)
        # We can connect to several endpoints if we desire, and receive from all.
        self.backend.connect('tcp://{}:{}'.format(self.outcoming_address, self.outcoming_port))

    def _get_game(self):
        return self.frontend.recv_string()

    def _send_result(self, result):
        self.backend.send_string(result)

    def run(self):
        self._init()
        
        home_wins = 0
        total_games = 0
        score_string = self._get_game()

        while score_string != END_TOKEN:
            score = AcummulatedScore.from_string(score_string)

            
            total_games += 1 
            if score.home_wins():
                home_wins += 1
            
            score_string = self._get_game()

        self._send_result("{}%".format(float(home_wins) / total_games * 100 ))
        self._send_result("END")
        self._close()

    def _close(self):
        from time import sleep
        sleep(20)
        
        self.frontend.close()
        self.backend.close()
        self.context.term()