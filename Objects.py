class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class Bomb:
    def __init__(self, scope=1):
        self.scope = scope

class Stone:
    def __init__(self, toughness=True):
        self.toughness = toughness

    def putStone(self):
        if self.toughness == True:
            return 2
        else:
            return 3
