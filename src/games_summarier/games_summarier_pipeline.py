from multiprocessing import Process
from collections import Counter
import zmq
from sink import Sink
from .games_summarier import GamesSummarier
from streamer_subscriber import StreamerSubscriber

class GamesSummarierPipeline(Process):

    def __init__(self, config, incoming_address, incoming_port):
        self.incoming_address = incoming_address
        self.incoming_port = incoming_port
        self.config = config
        super(GamesSummarierPipeline, self).__init__()


    def run(self):
        address_used_internally = self.config['address_used_internally']
        range_port_init = self.config['internal_range_port']
        
        input_streamer = StreamerSubscriber(self.incoming_address, self.incoming_port, address_used_internally, range_port_init, 1, 1)
        games_summarier = GamesSummarier(address_used_internally, range_port_init, address_used_internally, range_port_init + 1)
        sink = Sink(address_used_internally, range_port_init + 1, '%home-wins.txt')
        
        input_streamer.start()
        games_summarier.start()
        sink.start()
        
        input_streamer.join()
        games_summarier.join()
        sink.join()