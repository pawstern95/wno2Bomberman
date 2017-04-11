import random
import numpy as np
from Characters import Agent, Enemy
from Objects import Stone, Bomb, Direction


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
            x, y = self.agent.getPosition()
            value1 = self.board[x][y+1]
            if value1 != 2 and value1 != 3 and value1 != 4 and value1 != 6 and value1 != 13 and value1 != 15 and value1 != 17:
                self.takeOffAgent()
                self.agent.moveRight()
                if value1 == 8 or value1 == 9 or value1 == 10 or value1 == 11 or value1 == 12:
                    self.agent.kill()
                else:
                    self.putAgent()
        elif dir == Direction.LEFT:
            x, y = self.agent.getPosition()
            value2 = self.board[x][y-1]
            if value2 != 2 and value2 != 3 and value2 != 4 and value2 != 6 and value2 != 13 and value2 != 15 and value2 != 17:
                self.takeOffAgent()
                self.agent.moveLeft()
                if value2 == 8 or value2 == 9 or value2 == 10 or value2 == 11 or value2 == 12:
                    self.agent.kill()
                else:
                    self.putAgent()
        elif dir == Direction.UP:
            x, y = self.agent.getPosition()
            value3 = self.board[x-1][y]
            if value3 != 2 and value3 != 3 and value3 != 4 and value3 != 6 and value3 != 13 and value3 != 15 and value3 != 17:
                self.takeOffAgent()
                self.agent.moveUp()
                if value3 == 8 or value3 == 9 or value3 == 10 or value3 == 11 or value3 == 12:
                    self.agent.kill()
                else:
                    self.putAgent()
        elif dir == Direction.DOWN:
            x, y = self.agent.getPosition()
            value4 = self.board[x+1][y]
            if value4 != 2 and value4 != 3 and value4 != 4 and value4 != 6 and value4 != 13 and value4 != 15 and value4 != 17:
                self.takeOffAgent()
                self.agent.moveDown()
                if value4 == 8 or value4 == 9 or value4 == 10 or value4 == 11 or value4 == 12:
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
