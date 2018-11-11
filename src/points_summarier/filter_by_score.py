from multiprocessing import Process
import zmq

END_TOKEN = 'END'
class FilterByScore(Process):

    def __init__(self, points_filter, incoming_address, incoming_port, outgoing_address, outgoing_port):
        self.incoming_address = incoming_address
        self.incoming_port = incoming_port
        self.outgoing_address = outgoing_address
        self.outgoing_port = outgoing_port     
        self.points_filter = points_filter   
        super(FilterByScore, self).__init__()

    def _init(self):
        self.context = zmq.Context()
        self.frontend = self.context.socket(zmq.PULL)
        self.frontend.connect('tcp://{}:{}'.format(self.incoming_address, self.incoming_port))

        self.backend = self.context.socket(zmq.PUSH)
        self.backend.connect('tcp://{}:{}'.format(self.outgoing_address, self.outgoing_port))

    def _get_row(self):
        x = self.frontend.recv_json()

        return x

    def _send_shot(self, shot):
        self.backend.send_json(shot)

    def run(self):
        self._init()
        row = self._get_row()

        while row != END_TOKEN:
            if (int(row[1]) == int(self.points_filter)):
                self._send_shot(row)
            row = self._get_row()
            
            
        self._send_shot(END_TOKEN)
        print('Finished filter by score')
        self._close()

    def _close(self):
        from time import sleep
        sleep(60)
        
        self.frontend.close()
        self.backend.close()
        self.context.term()
