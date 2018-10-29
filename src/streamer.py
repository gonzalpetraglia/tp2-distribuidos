import zmq
from multiprocessing import Process

class Streamer(Process):

    def __init__(self, incoming_address, incoming_port, outgoing_address, outgoing_port, number_of_threads=1):
        self.incoming_port = incoming_port
        self.outgoing_port = outgoing_port
        self.incoming_address = incoming_address
        self.outgoing_address = outgoing_address
        self.number_of_threads = number_of_threads
        super(Streamer, self).__init__()

    def _get_message(self):
        return self.frontend.recv_pyobj()
    
    def _forward_message(self, message):
        self.backend.send_pyobj(message)

    def run(self):
        try:

            self.context = zmq.Context(self.number_of_threads)
            # Socket facing clients

            self.frontend = self.context.socket(zmq.PULL)
            self.frontend.bind("tcp://{}:{}".format(self.incoming_address, self.incoming_port))
            # Socket facing services
            self.backend = self.context.socket(zmq.PUSH)
            self.backend.bind("tcp://{}:{}".format(self.outgoing_address, self.outgoing_port))
        
            message = self._get_message()
            while message != 'END':
                self._forward_message(message)
                message = self._get_message()
                

            self._forward_message('END')
            
        except Exception as e:
            print (e)
            print ("bringing down zmq device")
        finally:
            self.frontend.close()
            self.backend.close()
            self.context.term()
