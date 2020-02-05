from time import time, sleep
from ai.board_state_tree import BoardStateTree
from ai.smart_evaluator import SmartEvaluator

timePerMove = 0.

class AiController:
    def __init__(self, board, gameManager, color, evaluator, depth = 2):
        self.board = board
        self.gameManager = gameManager
        self.color = color
        self.evaluator = evaluator
        self.depth = depth

    def getMove(self):
        minExitTime = time() + timePerMove
        move = self.chooseMove()
        sleep(max(0, minExitTime - time()))
        return move

    def update(self):
        chosenMove = self.chooseMove()
        self.gameManager.move(chosenMove)

    def chooseMove(self):
        stateTree = BoardStateTree.createTree(self.board, self.depth, self.gameManager, self.evaluator)
        bestMove = stateTree.getBestMove()
        return bestMove