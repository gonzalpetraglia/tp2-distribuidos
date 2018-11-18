from multiprocessing import Process
from collections import Counter
import zmq
import json

END_TOKEN = 'END'
class SumUpPlayers(Process):

    def __init__(self, incoming_address, incoming_port, outgoing_address, outgoing_port, number_of_aggregator):
        self.incoming_address = incoming_address
        self.incoming_port = incoming_port
        self.outgoing_address = outgoing_address
        self.outgoing_port = outgoing_port        
        self.number_of_aggregator = number_of_aggregator
        super(SumUpPlayers, self).__init__()

    def _init(self):
        self.context = zmq.Context()
        self.frontend = self.context.socket(zmq.SUB)
        self.frontend.connect('tcp://{}:{}'.format(self.incoming_address, self.incoming_port))
        self.frontend.setsockopt_string(zmq.SUBSCRIBE, str(self.number_of_aggregator))

        self.backend = self.context.socket(zmq.PUSH)
        self.backend.connect('tcp://{}:{}'.format(self.outgoing_address, self.outgoing_port))
        

    def _get_row(self):

        _, msg = self.frontend.recv_multipart()
        msg = msg.decode()
        if msg != END_TOKEN:
            msg = json.loads(msg)
        return msg

    def _send_player(self, result):
        self.backend.send_json(result)

    def run(self):
        self._init()

        row = self._get_row()


        players_points = Counter()
        while row != END_TOKEN:

            player = row[1]
            points = int(row[0])
            players_points.update({player: points})
            row = self._get_row()
            
        for player in players_points:
            self._send_player([player, players_points.get(player)])

        self._send_player(END_TOKEN)
        self._close()

    def _close(self):
        from time import sleep
        sleep(20)
        
        self.frontend.close()
        self.backend.close()
        self.context.term()



