from collections import Counter
import zmq


class Numerator(Process):


    def _init(self):
        self.context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind("tcp://127.0.0.1:5555")
        self.counter = Counter()

    def _run(self):
        while True:
                
            service_name = self.socket.recv_string()

            current_number = self.counter.get(service_name) 
            current_number = current_number if current_number is not None else 0

            self.counter.update({service_name: 1})

            self.socket.send_string(str(current_number))
        

    def _close(self):
        self.socket.close()
        self.context.term()