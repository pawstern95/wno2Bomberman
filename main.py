import numpy as np
from enum import Enum
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import random

# objects on board:
# 1 - agent
# 2 - indestractible stone
# 3 - destractible stone
# 4 - weak bomb
# 5 - agent with weak bomb
# 6 - strong bomb
# 7 - agent with strong bomb
# 8 - enemy

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class Bomb:
    def __init__(self, scope=1):
        self.scope = scope
        self.time = 3 #seconds

class Stone:
    def __init__(self, toughness=True):
        self.toughness = toughness

    def putStone(self):
        if self.toughness == True:
            return 2
        else:
            return 3


class Character:
    xPosition = 0
    yPosition = 0
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

    def isAlive(self):
        return self.destroyed

class Enemy(Character):
    def __init__(self):
        super()

class Agent(Character):
    # xPosition = 0
    # yPosition = 0
    bombs3 = []
    bombs1 = []
    # destroyed = False

    def addBombs(self, amount=5, scope=1):
        if scope == 1:
            for i in range(0, amount):
                self.bombs1.append(Bomb(scope=scope))
        else:
            for i in range(0, amount):
                self.bombs3.append(Bomb(scope=scope))

    def dropBomb1(self):
        if self.bombs1:
            self.bombs1.pop()
            return 5, False
        else:
            return 1, True

    def dropBomb3(self):
        if self.bombs3:
            self.bombs3.pop()
            return 7, False
        else:
            return 1, True


class Board:
    def __init__(self, agent, xSize = 40, ySize = 40):
        self.xSize = xSize
        self.ySize = ySize
        self.board = np.zeros((xSize, ySize))
        self.genBoard()
        self.agent = agent
        self.putAgent()
        self.genEnemies()

    def putAgent(self):
        x,y = self.agent.getPosition()
        self.board[x][y] = 1

    def genEnemies(self):
        self.enemy1 = Enemy()
        self.putEnemy(self.enemy1)
        self.enemy2 = Enemy()
        self.putEnemy(self.enemy2)
        self.enemy3 = Enemy()
        self.putEnemy(self.enemy3)
        self.enemy4 = Enemy()
        self.putEnemy(self.enemy4)
        self.enemy5 = Enemy()
        self.putEnemy(self.enemy5)

    def putEnemy(self, enemy):
        while True:
            x = random.randrange(1, self.xSize)
            y = random.randrange(1, self.ySize)
            if self.board[x][y] != 0:
                continue
            else:
                self.board[x][y] = 8
                enemy.setPosition(x, y)
                break

    def takeOffAgent(self):
        x, y = self.agent.getPosition()
        self.board[x][y] -= 1

    def destroyWithBomb(self, x, y, ran):
        for i in range(0, ran+1):
            if self.board[x][y+i] == 3 or self.board[x][y+i] == 4 or self.board[x][y+i] == 6:
                self.board[x][y+i] = 0
            elif self.board[x][y+i] == 1 or self.board[x][y+i] == 5 or self.board[x][y+i] == 7:
                self.board[x][y+i] = 0
                self.agent.kill()
            elif self.board[x][y+i] == 2:
                break
        for i in range(0, ran + 1):
            if self.board[x-i][y] == 3 or self.board[x-i][y] == 4 or self.board[x-i][y] == 6:
                self.board[x-i][y] = 0
            elif self.board[x-i][y] == 1 or self.board[x-i][y] == 5 or self.board[x-i][y] == 7:
                self.board[x-i][y] = 0
                self.agent.kill()
            elif self.board[x-i][y] == 2:
                break
        for i in range(0, ran + 1):
            if self.board[x+i][y] == 3 or self.board[x+i][y] == 4 or self.board[x+i][y] == 6:
                self.board[x+i][y] = 0
            elif self.board[x+i][y] == 1 or self.board[x+i][y] == 5 or self.board[x+i][y] == 7:
                self.board[x+i][y] = 0
                self.agent.kill()
            elif self.board[x+1][y] == 2:
                break
        for i in range(0, ran + 1):
            if self.board[x][y-i] == 3 or self.board[x][y-i] == 4 or self.board[x][y-i] == 6:
                self.board[x][y-i] = 0
            elif self.board[x][y - i] == 1 or self.board[x][y - i] == 5 or self.board[x][y - i] == 7:
                self.board[x][y-i] = 0
                self.agent.kill()
            elif self.board[x][y - i] == 2:
                break

    def dropBomb1(self):
        x, y = self.agent.getPosition()
        if self.board[x][y] == 1:
            value, empty = self.agent.dropBomb1()
            self.board[x][y] = value
        return x, y, empty


    def dropBomb3(self):
        x, y = self.agent.getPosition()
        if self.board[x][y] == 1:
            value, empty = self.agent.dropBomb3()
            self.board[x][y] = value
        return x, y, empty

    def moveAgent(self, dir):
        if dir == Direction.RIGHT:
            x,y = self.agent.getPosition()
            if (y < self.ySize - 1) and self.board[x][y+1] != 2 and self.board[x][y+1] != 3 and \
                            self.board[x][y+1] != 4 and self.board[x][y+1] != 6:
                self.takeOffAgent()
                self.agent.moveRight()
                self.putAgent()
        elif dir == Direction.LEFT:
            x, y = self.agent.getPosition()
            if y > 0 and self.board[x][y-1] != 2 and self.board[x][y-1] != 3 and \
                            self.board[x][y-1] != 4 and self.board[x][y-1] != 6:
                self.takeOffAgent()
                self.agent.moveLeft()
                self.putAgent()
        elif dir == Direction.UP:
            x, y = self.agent.getPosition()
            if x > 0 and self.board[x-1][y] != 2 and self.board[x-1][y] != 3 and \
                            self.board[x-1][y] != 4 and self.board[x-1][y] != 6:
                self.takeOffAgent()
                self.agent.moveUp()
                self.putAgent()
        elif dir == Direction.DOWN:
            x, y = self.agent.getPosition()
            if x < self.xSize-1 and self.board[x+1][y] != 2 and self.board[x+1][y] != 3 and \
                            self.board[x+1][y] != 4 and self.board[x+1][y] != 6:
                self.takeOffAgent()
                self.agent.moveDown()
                self.putAgent()

    def genBoard(self):
        for x in range(0, self.xSize):
            for y in range(0, self.ySize):
                if x%2 != 0:
                    if y%2 != 0:
                        self.board[x][y]=Stone().putStone()
                if self.board[x][y] != 2:
                    if (x, y) != (0, 0) and (x, y) != (0, 1) and (x, y) != (0, 2) and (x, y) != (0, 3) and (x, y) != (1, 0):
                        if random.randrange(0, 2) == 0:
                            self.board[x][y] = Stone(False).putStone()


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.agent = Agent()
        self.agent.addBombs(amount=50)
        self.agent.addBombs(amount=20, scope=3)
        self.board = Board(self.agent, 30, 30)
        self.displayBoard()
        self.timers = []

    def initUI(self):
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Event handler')
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Right:
            self.board.moveAgent(Direction.RIGHT)
            self.displayBoard()
        elif e.key() == Qt.Key_Left:
            self.board.moveAgent(Direction.LEFT)
            self.displayBoard()
        elif e.key() == Qt.Key_Up:
            self.board.moveAgent(Direction.UP)
            self.displayBoard()
        elif e.key() == Qt.Key_Down:
            self.board.moveAgent(Direction.DOWN)
            self.displayBoard()
        elif e.key() == Qt.Key_Space:
            x, y, empty = self.board.dropBomb1()
            if not empty:
                self.displayBoard()
                self.timers.append(QTimer())
                self.timers[len(self.timers) - 1].setInterval(3000)
                timer = self.timers[len(self.timers) - 1]
                timer.timeout.connect(lambda: self.board.destroyWithBomb(x, y, 1))
                timer.timeout.connect(self.displayBoard)
                timer.timeout.connect(timer.stop)
                timer.start()
        elif e.key() == Qt.Key_Alt:
            x, y, empty = self.board.dropBomb3()
            if not empty:
                self.displayBoard()
                self.timers.append(QTimer())
                self.timers[len(self.timers) - 1].setInterval(3000)
                timer = self.timers[len(self.timers) - 1]
                timer.timeout.connect(lambda: self.board.destroyWithBomb(x, y, 3))
                timer.timeout.connect(self.displayBoard)
                timer.timeout.connect(timer.stop)
                timer.start()


    def displayBoard(self):
        print('\n' * 100)

        if(self.board.agent.isAlive()):
            print('GAME OVER')
        else:
            array = []
            for x in range(0, self.board.xSize):
                row = ''
                for y in range(0, self.board.ySize):
                    row += str(self.board.board[x][y])[:1] + ' '
                array.append(row)
            for i in range(0, len(array)):
                print(array[i])




if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())



