import zmq
from multiprocessing import Process

END_TOKEN = 'END'

class StreamerSubscriber(Process):

    def __init__(self, incoming_address, incoming_port, outgoing_address, outgoing_port, number_of_publishers, number_of_pullers, number_of_threads=1):
        self.incoming_port = incoming_port
        self.outgoing_port = outgoing_port
        self.incoming_address = incoming_address
        self.outgoing_address = outgoing_address
        self.number_of_threads = number_of_threads
        self.number_of_publishers = number_of_publishers
        self.number_of_pullers = number_of_pullers
        super(StreamerSubscriber, self).__init__()

    def _get_message(self):
        return self.frontend.recv_json()
    
    def _forward_message(self, message):
        self.backend.send_json(message)

    def _init(self):
        self.context = zmq.Context(self.number_of_threads)
        # Socket facing clients

        self.frontend = self.context.socket(zmq.SUB)
        self.frontend.connect('tcp://{}:{}'.format(self.incoming_address, self.incoming_port))
        self.frontend.setsockopt_string(zmq.SUBSCRIBE, '')
    
        # Socket facing services
        self.backend = self.context.socket(zmq.PUSH)
        self.backend.bind("tcp://{}:{}".format(self.outgoing_address, self.outgoing_port))

    def run(self):
        try:
            self._init()
            accumulated_end_tokens = 0
            while accumulated_end_tokens < self.number_of_publishers:
                message = self._get_message()
                if message == END_TOKEN:
                    accumulated_end_tokens += 1
                    continue
                self._forward_message(message)
            
            print('Finishing streamer')
            for i in range(self.number_of_pullers):
                self._forward_message(END_TOKEN)
            
        except Exception as e:
            print (e)
            print ("bringing down zmq device")
        finally:
            from time import sleep
            sleep(60)
            self.frontend.close()
            self.backend.close()
            self.context.term()
