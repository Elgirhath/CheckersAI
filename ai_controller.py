import random
from time import time

timePerMove = 1.

class AiController():
    def __init__(self, board, gameManager, color):
        self.board = board
        self.gameManager = gameManager
        self.color = color
        self.callTime = None

    def getMove(self):
        if self.callTime == None:
            self.callTime = time()
        if time() - self.callTime >= timePerMove:
            self.callTime = None
            return self.choseMove()
        else:
            return None

    def update(self):
        chosenMove = self.choseMove()
        self.gameManager.move(chosenMove)

    def choseMove(self):
        allMoves = self.gameManager.getAllAvailableMoves()
        return random.choice(allMoves)