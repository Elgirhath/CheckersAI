from time import time, sleep
from ai.board_state_tree import BoardStateTree

timePerMove = 0.
depth = 4

class AiController:
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
        stateTree = BoardStateTree.createTree(self.board, depth, self.gameManager)
        bestMove = stateTree.getBestMove()
        return bestMove