from multiprocessing import Process
from collections import Counter
import zmq

from score import AcummulatedScore
END_TOKEN = 'END'
class SumUpGames(Process):

    def __init__(self, incoming_address, incoming_port, outgoing_address, outgoing_port, sink_address, sink_port):
        self.incoming_address = incoming_address
        self.incoming_port = incoming_port
        self.outgoing_address = outgoing_address
        self.outgoing_port = outgoing_port     
        self.sink_address = sink_address
        self.sink_port = sink_port   
        super(SumUpGames, self).__init__()

    def _init(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        self.socket.connect('tcp://{}:{}'.format(self.incoming_address, self.incoming_port))
        
        self.socket2 = self.context.socket(zmq.PUSH)
        self.socket2.bind('tcp://{}:{}'.format(self.outgoing_address, self.outgoing_port))
        
        self.socket3 = self.context.socket(zmq.PUSH)
        self.socket3.connect('tcp://{}:{}'.format(self.sink_address, self.sink_port))
        

    def _get_row(self):
        x = self.socket.recv_pyobj()
        return x

    def _send_result(self, result):
        self.socket2.send_string(result)

    def _send_match(self, result):
        self.socket3.send_string(result)

    def run(self):
        self._init()

        row = self._get_row()

        games = Counter()
        while row != 'END':
            date = row[0]
            home_team = row[1]
            away_team = row[2]
            points = row[3]
            shot_team =  row[4]
            key = '{}_{}_{}'.format(date, home_team, away_team)
            points =  int(row[3])
            if shot_team == home_team:
                acummulated_score = AcummulatedScore(points, 0)
            else:
                acummulated_score = AcummulatedScore(0, points)
            games.update({key: acummulated_score})
            row = self._get_row()

        for game in games:
            self._send_result(str(games.get(game)))
            self._send_match("{}, {}".format(game, games.get(game)))
            
        self._send_result('END')
        self._send_match('END')
        self._close()

    def _close(self):
        self.socket.close()
        self.socket2.close()
        self.socket3.close()
        self.context.term()



