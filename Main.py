from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import os
import threading
from Objects import Direction
from Characters import Agent
from Board import Board


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

class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.initGame()

        self.startButton = QPushButton('New Game', self)
        self.startButton.setGeometry(720, 120, 120, 50)
        self.startButton.clicked.connect(lambda: self.pauseButton.setText('Pause'))
        self.startButton.clicked.connect(self.initGame)

        self.pauseButton = QPushButton('Pause', self)
        self.pauseButton.setGeometry(720, 200, 120, 50)
        self.pauseButton.clicked.connect(self.pauseAction)

        self.highScoreButton = QPushButton('High Scores', self)
        self.highScoreButton.setGeometry(720, 280, 120, 50)

        font = QFont('Times', 22)
        self.scoreLabel = QLabel('Score: {0}'.format(self.board.score), self)
        self.scoreLabel.setGeometry(720, 0, 140, 100)
        self.scoreLabel.setFont(font)

        self.initUI()

    def pauseAction(self):
        if not self.paused:
            self.timer.stop()
            self.paused = True
            self.pauseButton.setText('Resume')
        else:
            self.timer.start()
            self.paused = False
            self.pauseButton.setText('Pause')


    def initUI(self):
        self.setGeometry(300, 30, 900, 700)
        self.setWindowTitle('Bomberman')
        self.show()

    def initGame(self):
        self.paused = False
        self.agent = Agent()
        self.agent.addBombs(amount=50)
        self.agent.addBombs(amount=30, scope=2)
        self.agent.addBombs(amount=15, scope=3)
        self.agent.addBombs(amount=10, scope=4)
        self.agent.addBombs(amount=5, scope=5)
        self.board = None
        self.board = Board(self.agent, 41, 41)
        self.timer = None
        self.timer = QTimer()
        self.timer.setInterval(700)
        self.mainTimer = None
        self.mainTimer = QTimer()
        self.mainTimer.setInterval(30)
        self.timers = []
        self.timer.timeout.connect(lambda: self.board.moveEnemy(self.board.enemy1))
        self.timer.timeout.connect(lambda: self.board.moveEnemy(self.board.enemy2))
        self.timer.timeout.connect(lambda: self.board.moveEnemy(self.board.enemy3))
        self.timer.timeout.connect(lambda: self.board.moveEnemy(self.board.enemy4))
        self.timer.timeout.connect(lambda: self.board.moveEnemy(self.board.enemy5))
        self.timer.start()
        self.mainTimer.timeout.connect(self.repaint)
        self.mainTimer.start()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        if not self.board.agent.isDead():
            self.drawBoard(qp)
            self.scoreLabel.setText('Score: {0}'.format(self.board.score))
        else:
            self.drawRectangle(qp)
        qp.end()

    def drawStone(self, qp, moveX, moveY, sizeX=15, sizeY=15):
        #black
        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        qp.setPen(col)
        qp.setBrush(QColor(60, 60, 60))
        qp.drawRect(moveX, moveY, sizeX, sizeY)

    def drawDestrStone(self, qp, moveX, moveY, sizeX=15, sizeY=15):
        #green
        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        qp.setPen(col)
        brush = QBrush()
        brush.setStyle(Qt.DiagCrossPattern)
        qp.setBrush(brush)

        qp.drawRect(moveX, moveY, sizeX, sizeY)

    def drawAgent(self, qp, moveX, moveY, sizeX=15, sizeY=15):
        #blue
        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        qp.drawPixmap(moveX, moveY, sizeX, sizeY, QPixmap(os.getcwd() + '\\agent.png'))

    def drawAgentWithBomb(self, qp, moveX, moveY, sizeX=15, sizeY=15):
        #cyan
        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        qp.setPen(col)
        qp.setBrush(QColor(255, 0, 255))
        qp.drawEllipse(moveX, moveY, sizeX, sizeY)

    def drawBomb(self, qp, moveX, moveY, sizeX=15, sizeY=15):
        #violet
        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        qp.setPen(col)
        qp.setBrush(QColor(255, 0, 0))
        qp.drawEllipse(moveX, moveY, sizeX, sizeY)

    def drawWhiteSpace(self, qp, moveX, moveY, sizeX=15, sizeY=15):
        #white
        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        qp.setPen(col)
        qp.setBrush(QColor(255, 255, 255))
        qp.drawRect(moveX, moveY, sizeX, sizeY)

    def drawEnemy(self, qp, moveX, moveY, sizeX=15, sizeY=15):
        #red
        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        qp.drawPixmap(moveX, moveY, sizeX, sizeY, QPixmap(os.getcwd() + '\\enemy.png'))

    def drawRectangle(self, qp):
        #white
        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        qp.setPen(col)
        qp.setBrush(QColor(100, 100, 100))
        qp.drawRect(0, 0, self.board.xSize*17, self.board.ySize*17)


    def drawBoard(self, qp):
        for x in range(0, self.board.xSize):
            for y in range(0, self.board.ySize):
                value = self.board.board[y][x]
                sizeX = 17
                sizeY = 17
                moveX = x*sizeX
                moveY = y*sizeY

                if value == 0:
                    self.drawWhiteSpace(qp, moveX, moveY, sizeX, sizeY)
                elif value == 1:
                    self.drawAgent(qp, moveX, moveY, sizeX, sizeY)
                elif value == 2:
                    self.drawStone(qp, moveX, moveY, sizeX, sizeY)
                elif value == 3:
                    self.drawDestrStone(qp, moveX, moveY, sizeX, sizeY)
                elif value == 4 or value == 6 or value == 13 or value == 15 or value == 17:
                    self.drawBomb(qp, moveX, moveY, sizeX, sizeY)
                elif value == 5 or value == 7 or value == 14 or value == 16 or value == 18:
                    self.drawAgentWithBomb(qp, moveX, moveY, sizeX, sizeY)
                elif value == 8 or value == 9 or value == 10 or value == 11 or value == 12:
                    self.drawEnemy(qp, moveX, moveY, sizeX, sizeY)


    def keyPressEvent(self, e):
        if not self.paused:
            if e.key() == Qt.Key_Right:
                self.board.moveAgent(Direction.RIGHT)
            elif e.key() == Qt.Key_Left:
                self.board.moveAgent(Direction.LEFT)
            elif e.key() == Qt.Key_Up:
                self.board.moveAgent(Direction.UP)
            elif e.key() == Qt.Key_Down:
                self.board.moveAgent(Direction.DOWN)
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

    def keyReleaseEvent(self, e):
        if not self.paused:
            if e.key() == Qt.Key_Right:
                self.board.moveAgent(Direction.RIGHT)
            elif e.key() == Qt.Key_Left:
                self.board.moveAgent(Direction.LEFT)
            elif e.key() == Qt.Key_Up:
                self.board.moveAgent(Direction.UP)
            elif e.key() == Qt.Key_Down:
                self.board.moveAgent(Direction.DOWN)

    def displayBoard(self):
        os.system("cls")

        if(self.board.agent.isDead()):
            print('GAME OVER')
            self.close()
        else:
            array = []
            for x in range(0, self.board.xSize):
                row = ''
                for y in range(0, self.board.ySize):
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



