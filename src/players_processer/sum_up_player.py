from multiprocessing import Process
from collections import Counter
import zmq

END_TOKEN = 'END'
class SumUpPlayers(Process):

    def __init__(self, incoming_address, incoming_port, outgoing_address, outgoing_port):
        self.incoming_address = incoming_address
        self.incoming_port = incoming_port
        self.outgoing_address = outgoing_address
        self.outgoing_port = outgoing_port        
        super(SumUpPlayers, self).__init__()

    def _init(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        self.socket.connect('tcp://{}:{}'.format(self.incoming_address, self.incoming_port))
        
        self.socket2 = self.context.socket(zmq.PUSH)
        self.socket2.connect('tcp://{}:{}'.format(self.outgoing_address, self.outgoing_port))
        

    def _get_row(self):

        x = self.socket.recv_pyobj()

        return x

    def _send_player(self, result):
        self.socket2.send_pyobj(result)

    def run(self):
        self._init()

        row = self._get_row()


        players_points = Counter()
        while row != 'END':

            player = row[1]
            points = int(row[0])
            players_points.update({player: points})
            row = self._get_row()
            
        for player in players_points:
            self._send_player([player, players_points.get(player)])

        self._send_player('END')
        self._close()

    def _close(self):
        self.socket.close()
        self.socket2.close()
        self.context.term()



