import zmq
from multiprocessing import Process

class PointsSummarier(Process):
    def __init__(self, points_filter, incoming_address, incoming_port):
        self.incoming_address = incoming_address
        self.incoming_port = incoming_port
        self.points_filter = points_filter
        super(PointsSummarier, self).__init__()

    def _init(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        # We can connect to several endpoints if we desire, and receive from all.
        self.socket.connect('tcp://{}:{}'.format(self.incoming_address, self.incoming_port))

        self.socket.setsockopt_string(zmq.SUBSCRIBE, '')

    def _get_row(self):
        return self.socket.recv_pyobj()

    def run(self):
        self._init()
        row = self._get_row()
        l2 = []
        while row != 'END':

            l2.append([row['current shot outcome'],
                    row['points']]) #send
            row = self._get_row()

        l3 = filter(lambda x: int(x[1]) == self.points_filter, l2)

        scored_shots = 0
        total_shots = 0


        for shot in l3:
            total_shots += 1 
            if shot[0] == 'SCORED':
                scored_shots += 1
            
        print('% {}pts scored: {}'.format(self.points_filter, float(scored_shots) / total_shots))


        self._close()

    def _close(self):
        self.socket.close()
        self.context.term()
