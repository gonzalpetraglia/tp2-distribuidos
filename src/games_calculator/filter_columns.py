from multiprocessing import Process
import zmq

END_TOKEN = 'END'
class FilterColumns(Process):

    def __init__(self, incoming_address, incoming_port, outgoing_address, outgoing_port):
        self.incoming_address = incoming_address
        self.incoming_port = incoming_port
        self.outgoing_address = outgoing_address
        self.outgoing_port = outgoing_port        
        super(FilterColumns, self).__init__()

    def _init(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect('tcp://{}:{}'.format(self.incoming_address, self.incoming_port))
        self.socket.setsockopt_string(zmq.SUBSCRIBE, '')
        
        self.socket2 = self.context.socket(zmq.PUSH)
        self.socket2.connect('tcp://{}:{}'.format(self.outgoing_address, self.outgoing_port))
        

    def _get_row(self):
        x = self.socket.recv_pyobj()
        return x

    def _send_filtered_columns(self, columns):
        self.socket2.send_pyobj(columns)

    def run(self):
        self._init()
        row = self._get_row()

        while row != 'END':
            self._send_filtered_columns([row['current shot outcome'],
                    row['date'],
                    row['home team'],
                    row['away team'],
                    row['points'],
                    row['shoot team']])

            row = self._get_row()

        self._send_filtered_columns('END')
        self._close()

    def _close(self):
        self.socket.close()
        self.socket2.close()
        self.context.term()
