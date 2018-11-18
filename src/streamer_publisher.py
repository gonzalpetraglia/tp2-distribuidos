import zmq
from multiprocessing import Process
from hashlib import md5
import json

END_TOKEN = 'END'

class StreamerPublisher(Process):

    def __init__(self, incoming_address, incoming_port, outgoing_address, outgoing_port, number_of_pushers, number_of_subscribers=None, _get_key=None, number_of_threads=1):
        self.incoming_port = incoming_port
        self.outgoing_port = outgoing_port
        self.incoming_address = incoming_address
        self.outgoing_address = outgoing_address
        self.number_of_threads = number_of_threads
        self.number_of_pushers = number_of_pushers
        self._get_key = _get_key
        self.number_of_subscribers = number_of_subscribers
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
 
        if self._get_key is None or self.number_of_subscribers is None:
            self.backend.send_json(message)
        else:
            key = self._get_key(message)
            hashed_key = str(int(md5(key.encode()).hexdigest(), 16) % self.number_of_subscribers)
            message_encoded = json.dumps(message).encode()
            self.backend.send_multipart([hashed_key.encode(), message_encoded])

    def _forward_end_message(self):
        if self._get_key is None or self.number_of_subscribers is None:
            self.backend.send_json(END_TOKEN)
        else:

            for i in range(self.number_of_subscribers):
                self.backend.send_multipart([str(i).encode(), END_TOKEN.encode()])


    def run(self):
        try:
            self._init()
            print ('inited publisher {} {}'.format(self.number_of_subscribers, self._get_key))
            accumulated_end_tokens = 0
            while accumulated_end_tokens < self.number_of_pushers:
                message = self._get_message()
                if message == END_TOKEN:
                    accumulated_end_tokens += 1
                    continue
                self._forward_message(message)
            
            self._forward_end_message()
            
        except Exception as e:
            print (e)
            print ("bringing down zmq device")
        finally:
            from time import sleep
            sleep(20)

            self.frontend.close()
            self.backend.close()
            self.context.term()
