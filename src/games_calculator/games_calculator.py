from multiprocessing import Process
from collections import Counter
import zmq

from score import AcummulatedScore
END_TOKEN = 'END'
class GamesCalculator(Process):

    def __init__(self, incoming_address, incoming_port):
        self.incoming_address = incoming_address
        self.incoming_port = incoming_port
        super(GamesCalculator, self).__init__()

    def _init(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        # We can connect to several endpoints if we desire, and receive from all.
        self.socket.connect('tcp://{}:{}'.format(self.incoming_address, self.incoming_port))
        self.socket.setsockopt_string(zmq.SUBSCRIBE, '')
        
        self.socket2 = self.context.socket(zmq.PUB)
        self.socket2.bind('tcp://{}:{}'.format('127.0.0.1', '2001'))
        

    def _get_row(self):
        return self.socket.recv_pyobj()

    def _send_game(self, result):
        self.socket2.send_pyobj(result)

    def run(self):
        self._init()
        row = self._get_row()
        l2 = []
        while row != 'END':

            l2.append([row['current shot outcome'],
                    row['date'],
                    row['home team'],
                    row['away team'],
                    row['points'],
                    row['shoot team']])# send
            row = self._get_row()



        l3 = map(lambda x: x[1:], filter(lambda x: x[0] == 'SCORED', l2)) # filter column that is redundant #send

        games = Counter()
        for l in l3:
            date = l[0]
            home_team = l[1]
            away_team = l[2]
            points = l[3]
            shot_team =  l[4]
            key = '{}_{}_{}'.format(date, home_team, away_team)
            points =  int(l[3])
            if shot_team == home_team:
                acummulated_score = AcummulatedScore(points, 0)
            else:
                acummulated_score = AcummulatedScore(0, points)
            games.update({key: acummulated_score})

        print('Games: ' + str(games))

        for game in games:
            self._send_game(games.get(game))
        self._send_game('END')
        self._close()

    def _close(self):
        self.socket.close()
        self.socket2.close()
        self.context.term()
