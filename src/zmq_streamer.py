import zmq
from multiprocessing import Process

class Streamer(Process):

    def __init__(self, incoming_port, outgoing_port, incoming_address='*', outgoing_address='*', number_of_threads=1):
        self.incoming_port = incoming_port
        self.outgoing_port = outgoing_port
        self.incoming_address = incoming_address
        self.outgoing_address = outgoing_address

    def run(self):
        try:
            context = zmq.Context(self.number_of_threads)
            # Socket facing clients
            frontend = context.socket(zmq.PULL)
            frontend.bind("tcp://{}:{}".format(self.incoming_address, self.incoming_port))
            # Socket facing services
            backend = context.socket(zmq.PUSH)
            backend.bind("tcp://{}:{}".format(self.outgoing_address, self.outgoing_port))

            zmq.device(zmq.STREAMER, frontend, backend)
        except Exception as e:
            print (e)
            print ("bringing down zmq device")
        finally:
            frontend.close()
            backend.close()
            context.term()
