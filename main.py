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



