from multiprocessing import Process
from collections import Counter
import zmq
from sink import Sink
from .games_summarier import GamesSummarier
from streamer import Streamer

class GamesSummarierPipeline(Process):

    def __init__(self, incoming_address, incoming_port, range_port_init):
        self.incoming_address = incoming_address
        self.incoming_port = incoming_port
        self.range_port_init = range_port_init
        super(GamesSummarierPipeline, self).__init__()


    def run(self):

        input_streamer = Streamer(self.incoming_address, self.incoming_port, '127.0.0.1', self.range_port_init, 10, 1)
        games_summarier = GamesSummarier('127.0.0.1', self.range_port_init, '127.0.0.1', self.range_port_init + 1)
        sink = Sink('127.0.0.1', self.range_port_init + 1, '%home-wins.txt')
        
        input_streamer.start()
        games_summarier.start()
        sink.start()
        
        input_streamer.join()
        games_summarier.join()
        sink.join()