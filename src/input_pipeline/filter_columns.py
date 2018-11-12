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
        self.frontend = self.context.socket(zmq.PULL)
        self.frontend.connect('tcp://{}:{}'.format(self.incoming_address, self.incoming_port))
        
        self.backend = self.context.socket(zmq.PUSH)
        self.backend.connect('tcp://{}:{}'.format(self.outgoing_address, self.outgoing_port))
        

    def _get_row(self):
        x = self.frontend.recv_json()
        return x

    def _send_filtered_columns(self, columns):
        self.backend.send_json(columns)

    def run(self):
        self._init()
        row = self._get_row()

        while row != END_TOKEN:
            self._send_filtered_columns(
                { 'current shot outcome': row['current shot outcome'],
                  'date': row['date'],
                  'home team': row['home team'],
                  'away team': row['away team'],
                  'points': row['points'],
                  'shoot team': row['shoot team'],
                  'shoot player': row['shoot player']})

            row = self._get_row()
            print(row)

        self._send_filtered_columns(END_TOKEN)
        self._close()
        print('Finished filter columns')

    def _close(self):
        from time import sleep
        sleep(20)
        
        self.frontend.close()
        self.backend.close()
        self.context.term()