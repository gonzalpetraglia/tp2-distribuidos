import zmq
from multiprocessing import Process

class Streamer(Process):

    def __init__(self, incoming_address, incoming_port, outgoing_address, outgoing_port, number_of_pushers, number_of_pullers, number_of_threads=1):
        self.incoming_port = incoming_port
        self.outgoing_port = outgoing_port
        self.incoming_address = incoming_address
        self.outgoing_address = outgoing_address
        self.number_of_threads = number_of_threads
        self.number_of_pushers = number_of_pushers
        self.number_of_pullers = number_of_pullers
        super(Streamer, self).__init__()

    def _get_message(self):
        return self.frontend.recv_json()
    
    def _forward_message(self, message):
        self.backend.send_json(message)

    def run(self):
        try:

            self.context = zmq.Context(self.number_of_threads)
            # Socket facing clients

            self.socket = self.context.socket(zmq.SUB)
            self.socket.connect('tcp://{}:{}'.format(self.incoming_address, self.incoming_port))
            self.socket.setsockopt_string(zmq.SUBSCRIBE, '')
        
            # Socket facing services
            self.backend = self.context.socket(zmq.PUSH)
            self.backend.bind("tcp://{}:{}".format(self.outgoing_address, self.outgoing_port))
    
            accumulated_end_tokens = 0
            while accumulated_end_tokens < self.number_of_pushers:
                message = self._get_message()
                print(message)
                if message == 'END':
                    accumulated_end_tokens += 1
                    print("Received {} ENDS. Total {}".format(accumulated_end_tokens, self.number_of_pushers))
                    continue
                self._forward_message(message)
            
            print('Finishing streamer')
            for i in range(self.number_of_pullers):
                self._forward_message('END')
            
        except Exception as e:
            print (e)
            print ("bringing down zmq device")
        finally:
            self.frontend.close()
            self.backend.close()
            self.context.term()