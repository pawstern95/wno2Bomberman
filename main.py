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
# 4 - bomb1
# 5 - agent with bomb1
# 6 - bomb3
# 7 - agent with bomb3
# 8 - enemy1
# 9 - enemy2
# 10 - enemy3
# 11 - enemy4
# 12 - enemy5
# 13 - bomb2
# 14 - agent with bomb2
# 15 - bomb4
# 16 - agent with bomb4
# 17 - bomb5
# 18 - agent with bomb5

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


class Board:
    def __init__(self, agent, xSize = 41, ySize = 41):
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
        self.enemy1 = Enemy(1)
        self.putEnemy(self.enemy1)
        self.enemy2 = Enemy(2)
        self.putEnemy(self.enemy2)
        self.enemy3 = Enemy(3)
        self.putEnemy(self.enemy3)
        self.enemy4 = Enemy(4)
        self.putEnemy(self.enemy4)
        self.enemy5 = Enemy(5)
        self.putEnemy(self.enemy5)

    def putEnemy(self, enemy):
        while True:
            x = random.randrange(1, self.xSize)
            y = random.randrange(1, self.ySize)
            if self.board[x][y] != 0:
                continue
            else:
                if enemy.id == 1:
                    self.board[x][y] = 8
                elif enemy.id == 2:
                    self.board[x][y] = 9
                elif enemy.id == 3:
                    self.board[x][y] = 10
                elif enemy.id == 4:
                    self.board[x][y] = 11
                elif enemy.id == 5:
                    self.board[x][y] = 12
                enemy.setPosition(x, y)
                break

    def takeOffAgent(self):
        x, y = self.agent.getPosition()
        self.board[x][y] -= 1

    def destroyWithBomb(self, x, y, ran):
        for i in range(0, ran+1):
            value1 = self.board[x][y+i]
            if value1 == 3 or value1 == 4 or value1 == 6 or value1 == 13 or value1 == 15 or value1 == 17:
                self.board[x][y+i] = 0
            elif value1 == 1 or value1 == 5 or value1 == 7 or value1 == 14 or value1 == 16 or value1 == 18:
                self.board[x][y+i] = 0
                self.agent.kill()
            elif value1 == 8:
                self.board[x][y+i] = 0
                self.enemy1.kill()
            elif value1 == 9:
                self.board[x][y+i] = 0
                self.enemy2.kill()
            elif value1 == 10:
                self.board[x][y+i] = 0
                self.enemy3.kill()
            elif value1 == 11:
                self.board[x][y+i] = 0
                self.enemy4.kill()
            elif value1 == 12:
                self.board[x][y+i] = 0
                self.enemy5.kill()
            elif value1 == 2:
                break
        for i in range(0, ran + 1):
            value2 = self.board[x-i][y]
            if value2 == 3 or value2 == 4 or value2 == 6 or value2 == 13 or value2 == 15 or value2 == 17:
                self.board[x-i][y] = 0
            elif value2 == 1 or value2 == 5 or value2 == 7 or value2 == 14 or value2 == 16 or value2 == 18:
                self.board[x-i][y] = 0
                self.agent.kill()
            elif value2 == 8:
                self.board[x-i][y] = 0
                self.enemy1.kill()
            elif value2 == 9:
                self.board[x-i][y] = 0
                self.enemy2.kill()
            elif value2 == 10:
                self.board[x-i][y] = 0
                self.enemy3.kill()
            elif value2 == 11:
                self.board[x-i][y] = 0
                self.enemy4.kill()
            elif value2 == 12:
                self.board[x-i][y] = 0
                self.enemy5.kill()
            elif value2 == 2:
                break
        for i in range(0, ran + 1):
            value3 = self.board[x+i][y]
            if value3 == 3 or value3 == 4 or value3 == 6 or value3 == 13 or value3 == 15 or value3 == 17:
                self.board[x+i][y] = 0
            elif value3 == 1 or value3 == 5 or value3 == 7 or value3 == 14 or value3 == 16 or value3 == 18:
                self.board[x+i][y] = 0
                self.agent.kill()
            elif value3 == 8:
                self.board[x+i][y] = 0
                self.enemy1.kill()
            elif value3 == 9:
                self.board[x+i][y] = 0
                self.enemy2.kill()
            elif value3 == 10:
                self.board[x+i][y] = 0
                self.enemy3.kill()
            elif value3 == 11:
                self.board[x+i][y] = 0
                self.enemy4.kill()
            elif value3 == 12:
                self.board[x+i][y] = 0
                self.enemy5.kill()
            elif value3 == 2:
                break
        for i in range(0, ran + 1):
            value4 = self.board[x][y-i]
            if value4 == 3 or value4 == 4 or value4 == 6 or value4 == 13 or value4 == 15 or value4 == 17:
                self.board[x][y-i] = 0
            elif value4 == 1 or value4 == 5 or value4 == 7 or value4 == 14 or value4 == 16 or value4 == 18:
                self.board[x][y-i] = 0
                self.agent.kill()
            elif value4 == 8:
                self.board[x][y-i] = 0
                self.enemy1.kill()
            elif value4 == 9:
                self.board[x][y-i] = 0
                self.enemy2.kill()
            elif value4 == 10:
                self.board[x][y-i] = 0
                self.enemy3.kill()
            elif value4 == 11:
                self.board[x][y-i] = 0
                self.enemy4.kill()
            elif value4 == 12:
                self.board[x][y-i] = 0
                self.enemy5.kill()
            elif value4 == 2:
                break

    def dropBomb1(self):
        x, y = self.agent.getPosition()
        if self.board[x][y] == 1:
            value, empty = self.agent.dropBomb1()
            self.board[x][y] = value
        return x, y, empty

    def dropBomb2(self):
        x, y = self.agent.getPosition()
        if self.board[x][y] == 1:
            value, empty = self.agent.dropBomb2()
            self.board[x][y] = value
        return x, y, empty

    def dropBomb4(self):
        x, y = self.agent.getPosition()
        if self.board[x][y] == 1:
            value, empty = self.agent.dropBomb4()
            self.board[x][y] = value
        return x, y, empty

    def dropBomb5(self):
        x, y = self.agent.getPosition()
        if self.board[x][y] == 1:
            value, empty = self.agent.dropBomb5()
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
            if self.board[x][y+1] != 2 and self.board[x][y+1] != 3 and \
                            self.board[x][y+1] != 4 and self.board[x][y+1] != 6:
                self.takeOffAgent()
                self.agent.moveRight()
                if self.board[x][y+1] == 8 or self.board[x][y+1] == 9 or self.board[x][y+1] == 10 or\
                            self.board[x][y+1] == 11 or self.board[x][y+1] == 12:
                    self.agent.kill()
                else:
                    self.putAgent()
        elif dir == Direction.LEFT:
            x, y = self.agent.getPosition()
            if self.board[x][y-1] != 2 and self.board[x][y-1] != 3 and \
                            self.board[x][y-1] != 4 and self.board[x][y-1] != 6:
                self.takeOffAgent()
                self.agent.moveLeft()
                if self.board[x][y-1] == 8 or self.board[x][y-1] == 9 or self.board[x][y-1] == 10 or\
                            self.board[x][y-1] == 11 or self.board[x][y-1] == 12:
                    self.agent.kill()
                else:
                    self.putAgent()
        elif dir == Direction.UP:
            x, y = self.agent.getPosition()
            if self.board[x-1][y] != 2 and self.board[x-1][y] != 3 and \
                            self.board[x-1][y] != 4 and self.board[x-1][y] != 6:
                self.takeOffAgent()
                self.agent.moveUp()
                if self.board[x-1][y] == 8 or self.board[x-1][y] == 9 or self.board[x-1][y] == 10 or\
                            self.board[x-1][y] == 11 or self.board[x-1][y] == 12:
                    self.agent.kill()
                else:
                    self.putAgent()
        elif dir == Direction.DOWN:
            x, y = self.agent.getPosition()
            if self.board[x+1][y] != 2 and self.board[x+1][y] != 3 and \
                            self.board[x+1][y] != 4 and self.board[x+1][y] != 6:
                self.takeOffAgent()
                self.agent.moveDown()
                if self.board[x+1][y] == 8 or self.board[x+1][y] == 9 or self.board[x+1][y] == 10 or\
                            self.board[x+1][y] == 11 or self.board[x+1][y] == 12:
                    self.agent.kill()
                else:
                    self.putAgent()


    def moveEnemy(self, enemy):
        if not enemy.isDead():
            x, y = enemy.getPosition()
            if enemy.direction == 1:
                if self.board[x][y+1] == 0:
                    enemy.moveRight()
                    self.board[x][y] = 0
                    self.board[x][y+1] = enemy.id + 7
                elif self.board[x][y+1] == 1:
                    self.agent.kill()
                else:
                    enemy.direction = 3
            elif enemy.direction == 2:
                if self.board[x][y-1] == 0:
                    enemy.moveLeft()
                    self.board[x][y] = 0
                    self.board[x][y - 1] = enemy.id + 7
                elif self.board[x][y-1] == 1:
                    self.agent.kill()
                else:
                    enemy.direction = 4
            elif enemy.direction == 3:
                if self.board[x-1][y] == 0:
                    enemy.moveUp()
                    self.board[x][y] = 0
                    self.board[x-1][y] = enemy.id + 7
                elif self.board[x-1][y] == 1:
                    self.agent.kill()
                else:
                    enemy.direction = 2
            elif enemy.direction == 4:
                if self.board[x+1][y] == 0:
                    enemy.moveDown()
                    self.board[x][y] = 0
                    self.board[x+1][y] = enemy.id + 7
                elif self.board[x+1][y] == 1:
                    self.agent.kill()
                else:
                    enemy.direction = 1

    def genBoard(self):
        for x in range(0, self.xSize):
            for y in range(0, self.ySize):
                if x == 0 or y == 0 or x == self.xSize-1 or y == self.ySize-1:
                    self.board[x][y]=Stone().putStone()
                if x%2 == 0:
                    if y%2 == 0:
                        self.board[x][y]=Stone().putStone()
                if self.board[x][y] != 2:
                    if (x, y) != (1, 1) and (x, y) != (1, 2) and (x, y) != (1, 3) and (x, y) != (1, 4) and (x, y) != (2, 1):
                        if random.randrange(0, 4) == 0:
                            self.board[x][y] = Stone(toughness=False).putStone()


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.agent = Agent()
        self.agent.addBombs(amount=50)
        self.agent.addBombs(amount=30, scope=2)
        self.agent.addBombs(amount=15, scope=3)
        self.agent.addBombs(amount=10, scope=4)
        self.agent.addBombs(amount=5, scope=5)
        self.board = Board(self.agent,31,31)
        #self.displayBoard()
        self.timers = []
        self.timer = QTimer()
        self.timer.setInterval(700)
        self.timer.timeout.connect(lambda: self.board.moveEnemy(self.board.enemy1))
        self.timer.timeout.connect(lambda: self.board.moveEnemy(self.board.enemy2))
        self.timer.timeout.connect(lambda: self.board.moveEnemy(self.board.enemy3))
        self.timer.timeout.connect(lambda: self.board.moveEnemy(self.board.enemy4))
        self.timer.timeout.connect(lambda: self.board.moveEnemy(self.board.enemy5))
        self.timer.timeout.connect(self.displayBoard)
        self.timer.start()

    def initUI(self):
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Bomberman')
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Right:
            self.board.moveAgent(Direction.RIGHT)
            #self.displayBoard()
        elif e.key() == Qt.Key_Left:
            self.board.moveAgent(Direction.LEFT)
            #self.displayBoard()
        elif e.key() == Qt.Key_Up:
            self.board.moveAgent(Direction.UP)
            #self.displayBoard()
        elif e.key() == Qt.Key_Down:
            self.board.moveAgent(Direction.DOWN)
            #self.displayBoard()
        elif e.key() == Qt.Key_Z:
            x, y, empty = self.board.dropBomb1()
            if not empty:
                self.timers.append(QTimer())
                self.timers[len(self.timers) - 1].setInterval(3000)
                timer = self.timers[len(self.timers) - 1]
                timer.timeout.connect(lambda: self.board.destroyWithBomb(x, y, 1))
                timer.timeout.connect(timer.stop)
                timer.start()
        elif e.key() == Qt.Key_X:
            x, y, empty = self.board.dropBomb2()
            if not empty:
                self.timers.append(QTimer())
                self.timers[len(self.timers) - 1].setInterval(3000)
                timer = self.timers[len(self.timers) - 1]
                timer.timeout.connect(lambda: self.board.destroyWithBomb(x, y, 2))
                timer.timeout.connect(timer.stop)
                timer.start()
        elif e.key() == Qt.Key_C:
            x, y, empty = self.board.dropBomb3()
            if not empty:
                self.timers.append(QTimer())
                self.timers[len(self.timers) - 1].setInterval(3000)
                timer = self.timers[len(self.timers) - 1]
                timer.timeout.connect(lambda: self.board.destroyWithBomb(x, y, 3))
                timer.timeout.connect(timer.stop)
                timer.start()
        elif e.key() == Qt.Key_V:
            x, y, empty = self.board.dropBomb4()
            if not empty:
                self.timers.append(QTimer())
                self.timers[len(self.timers) - 1].setInterval(3000)
                timer = self.timers[len(self.timers) - 1]
                timer.timeout.connect(lambda: self.board.destroyWithBomb(x, y, 4))
                timer.timeout.connect(timer.stop)
                timer.start()
        elif e.key() == Qt.Key_B:
            x, y, empty = self.board.dropBomb5()
            if not empty:
                self.timers.append(QTimer())
                self.timers[len(self.timers) - 1].setInterval(3000)
                timer = self.timers[len(self.timers) - 1]
                timer.timeout.connect(lambda: self.board.destroyWithBomb(x, y, 5))
                timer.timeout.connect(timer.stop)
                timer.start()


    def displayBoard(self):
        print('\n' * 100)

        if(self.board.agent.isDead()):
            print('GAME OVER')
            self.close()
        else:
            array = []
            for x in range(0, self.board.xSize):
                row = ''
                for y in range(0, self.board.ySize):
                    #row += str(self.board.board[x][y])[:1] + ' '
                    value = str(self.board.board[x][y])[:2]
                    if value == '0.':
                        row += '  '
                    elif value == '1.':
                        row += 'p '
                    elif value == '2.':
                        row += '# '
                    elif value == '3.':
                        row += '* '
                    elif value == '4.' or value == '6.' or value == '13' or value == '15' or value == '17':
                        row += 'b '
                    elif value == '5.' or value == '7.' or value == '14' or value == '16' or value == '18':
                        row += 'r '
                    elif value == '8.':
                        row += 'e '
                    elif value == '9.':
                        row += 'e '
                    elif value == '10':
                        row += 'e '
                    elif value == '11':
                        row += 'e '
                    elif value == '12':
                        row += 'e '
                array.append(row)
            for i in range(0, len(array)):
                print(array[i])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())



