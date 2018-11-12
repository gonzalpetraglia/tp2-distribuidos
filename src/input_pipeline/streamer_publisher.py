import zmq
from multiprocessing import Process

END_TOKEN = 'END'

class StreamerPublisher(Process):

    def __init__(self, incoming_address, incoming_port, outgoing_address, outgoing_port, number_of_pushers, number_of_threads=1):
        self.incoming_port = incoming_port
        self.outgoing_port = outgoing_port
        self.incoming_address = incoming_address
        self.outgoing_address = outgoing_address
        self.number_of_threads = number_of_threads
        self.number_of_pushers = number_of_pushers
        super(StreamerPublisher, self).__init__()

    def _init(self):
        self.context = zmq.Context(self.number_of_threads)
        # Socket facing clients

        self.frontend = self.context.socket(zmq.PULL)
        self.frontend.bind('tcp://{}:{}'.format(self.incoming_address, self.incoming_port))
    
        # Socket facing services
        self.backend = self.context.socket(zmq.PUB)
        self.backend.bind("tcp://{}:{}".format(self.outgoing_address, self.outgoing_port))

    def _get_message(self):
        return self.frontend.recv_json()
    
    def _forward_message(self, message):
        self.backend.send_json(message)

    def run(self):
        try:
            self._init()
            
            accumulated_end_tokens = 0
            while accumulated_end_tokens < self.number_of_pushers:
                message = self._get_message()
                if message == END_TOKEN:
                    accumulated_end_tokens += 1
                    continue
                self._forward_message(message)
            
            self._forward_message(END_TOKEN)
            
        except Exception as e:
            print (e)
            print ("bringing down zmq device")
        finally:
            from time import sleep
            sleep(20)

            self.frontend.close()
            self.backend.close()
            self.context.term()
