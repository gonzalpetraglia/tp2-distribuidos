from os import listdir, environ
from os.path import isfile, join, dirname
from re import match
import csv
from collections import Counter

class AcummulatedScore(object):

    def __init__(self, home_points, away_points):
        self.home_points = home_points
        self.away_points = away_points

    def __add__(self, another_score):
        if another_score == 0: # NULL Element
            return self + AcummulatedScore(0, 0)
        delta_home_points = another_score.home_points
        delta_away_points = another_score.away_points
        return AcummulatedScore(self.home_points + delta_home_points, self.away_points + delta_away_points )
    
    def __str__(self):
        return '{}-{}'.format(self.home_points, self.away_points)

    def __repr__(self):
        return self.__str__()

from bisect import insort_left

class RankingCandidate():
    def __init__(self, id, points):
        self.id = id
        self.points = points
    
    def __le__(self, another):
        return self.points <= another.points

    def __le__(self, another):
        return self.points < another.points

    def __ge__(self, another):
        return self.points >= another.points

    def __gt__(self, another):
        return self.points > another.points
    
    def __repr__(self):
        return '{}: {}'.format(self.id.__repr__(), self.points.__repr__())

class Ranking():
    def __init__(self, places):
        self.places = int(places)
        self.ranking = []
        self.min = None
        self.left_places = self.places

    def consider(self, candidate):
        if self.min is None: # Initializer
            self.min = candidate.points
        
        if candidate.points <= self.min and self.left_places == 0:
            return
        
        insort_left(self.ranking, candidate)
        self.left_places -= 1 
        if self.left_places < 0:
            self.ranking = self.ranking[1:]
            self.left_places += 1

    def __repr__(self):
        return list(reversed(self.ranking)).__repr__()
        

# Input 

INPUT_FILES_DIRECTORY = environ.get('INPUT_FILES_DIRECTORY', join(dirname(__file__), '../../shot-log'))

files_names = [join(INPUT_FILES_DIRECTORY, entry)  for entry in listdir(INPUT_FILES_DIRECTORY) if match(r'^shot log \w{3}\.csv$', entry)]
l1 = []
for file_name in files_names:
    csv_team = match(r'.*shot log (\w{3})\.csv$', file_name).group(1)
    with open(file_name, 'r') as f:
        shot_logs_reader = csv.DictReader(f)
        for line in shot_logs_reader: 
            line['shoot team'] = csv_team
            l1.append(line) #send

## Input


# Res 1
l2 = []
for l in l1:
    l2.append([l['current shot outcome'],
               l['date'],
               l['home team'],
               l['away team'],
               l['points'],
               l['shoot team']])# send


l3 = map(lambda x: x[1:], filter(lambda x: x[0] == 'SCORED', l2)) # filter column that is redundant #send

c = Counter()
for l in l3:
    date = l[0]
    home_team = l[1]
    away_team = l[2]
    points = l[3]
    shot_team =  l[4]
    key = '{}_{}_{}'.format(l[0], l[1], l[2], l[4])
    points =  int(l[3])
    if shot_team == home_team:
        acummulated_score = AcummulatedScore(points, 0)
    else:
        acummulated_score = AcummulatedScore(0, points)
    c.update({key: acummulated_score})

print(c)



## Res 1



# Res 2

l2 = []
for l in l1:
    l2.append([l['current shot outcome'],
               l['points'],
               l['shoot player']]) #send


l3 = map(lambda x: x[1:], filter(lambda x: x[0] == 'SCORED', l2)) # filter column that is redundant #send

c = Counter()
for l in l3:
    player = l[1]
    points = int(l[0])
    c.update({player: points})


ranking = Ranking(10)
for player in c:
    ranking.consider(RankingCandidate(player, c.get(player)))

print(ranking)
## Res 2



