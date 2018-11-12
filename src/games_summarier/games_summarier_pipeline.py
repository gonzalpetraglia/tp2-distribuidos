from multiprocessing import Process
from collections import Counter
from .games_summarier import GamesSummarier
import zmq
from sink import Sink


class GamesSummarierPipeline(Process):

    def __init__(self, incoming_address, incoming_port, range_port_init):
        self.incoming_address = incoming_address
        self.incoming_port = incoming_port
        self.range_port_init = range_port_init
        super(GamesSummarierPipeline, self).__init__()


    def run(self):
            
        games_summarier = GamesSummarier(self.incoming_address, self.incoming_port, '127.0.0.1', self.range_port_init)
        sink = Sink('127.0.0.1', self.range_port_init, '%home-wins.txt')
        
        games_summarier.start()
        sink.start()
        
        games_summarier.join()
        sink.join()