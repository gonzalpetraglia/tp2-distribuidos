
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

    def home_wins(self):
        return self.home_points > self.away_points

    @classmethod
    def from_string(cls, string):
        print(string)
        return cls(string.split('-')[0], string.split('-')[1])