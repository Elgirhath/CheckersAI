import random
from time import time, sleep

timePerMove = 0.

class RandomController:
    def __init__(self, board, gameManager, color):
        self.board = board
        self.gameManager = gameManager
        self.color = color

    def getMove(self):
        minExitTime = time() + timePerMove
        move = self.choseMove()
        sleep(max(0, minExitTime - time()))
        return move

    def update(self):
        chosenMove = self.choseMove()
        self.gameManager.move(chosenMove)

    def choseMove(self):
        allMoves = self.gameManager.getAllAvailableMoves()
        return random.choice(allMoves)