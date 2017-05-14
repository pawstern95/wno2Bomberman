from Objects import Bomb

class Character:
    xPosition = 1
    yPosition = 1
    destroyed = False

    def getPosition(self):
        return self.xPosition, self.yPosition

    def setPosition(self, xPos, yPos):
        self.xPosition = xPos
        self.yPosition = yPos

    def moveRight(self):
        x,y = self.getPosition()
        self.setPosition(x, y+1)

    def moveLeft(self):
        x,y = self.getPosition()
        self.setPosition(x, y-1)

    def moveUp(self):
        x,y = self.getPosition()
        self.setPosition(x-1, y)

    def moveDown(self):
        x,y = self.getPosition()
        self.setPosition(x+1, y)

    def kill(self):
        self.destroyed = True

    def isDead(self):
        return self.destroyed

class Enemy(Character):

    def __init__(self, id):
        self.id = id
        self.direction = 1

class Agent(Character):
    bombs5 = []
    bombs4 = []
    bombs3 = []
    bombs2 = []
    bombs1 = []
    direction = 1

    def addBombs(self, amount=5, scope=1):
        if scope == 1:
            for i in range(0, amount):
                self.bombs1.append(Bomb(scope=scope))
        elif scope == 2:
            for i in range(0, amount):
                self.bombs2.append(Bomb(scope=scope))
        elif scope == 3:
            for i in range(0, amount):
                self.bombs3.append(Bomb(scope=scope))
        elif scope == 4:
            for i in range(0, amount):
                self.bombs4.append(Bomb(scope=scope))
        elif scope == 5:
            for i in range(0, amount):
                self.bombs5.append(Bomb(scope=scope))

    def dropBomb1(self):
        if self.bombs1:
            self.bombs1.pop()
            return 5, False
        else:
            return 1, True

    def dropBomb2(self):
        if self.bombs2:
            self.bombs2.pop()
            return 14, False
        else:
            return 1, True

    def dropBomb4(self):
        if self.bombs1:
            self.bombs1.pop()
            return 16, False
        else:
            return 1, True

    def dropBomb5(self):
        if self.bombs1:
            self.bombs1.pop()
            return 18, False
        else:
            return 1, True

    def dropBomb3(self):
        if self.bombs3:
            self.bombs3.pop()
            return 7, False
        else:
            return 1, True