class TargetCame(object):
    def __init__(self, target):
        self.target = target

class TargetLeft(object):
    def __init__(self, target):
        self.target = target

class TargetDestroyed(object):
    def __init__(self, target):
        self.target = target

class PlayerScored(object):
    def __init__(self, address, points):
        self.address = address
        self.points = points

class GameOver(object):
    def __init__(self, winner):
        self.winner = winner
