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
    
        