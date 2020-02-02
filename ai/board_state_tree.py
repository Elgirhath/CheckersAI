import math
from enum import Enum

import ai.virtualizer as virtualizer
from ai.evaluate_engine import Evaluator
from player_color import PlayerColor
from game_data import GameState
import game_settings

class Type(Enum):
    Maximizer = False
    Minimizer = True

class BoardStateTree:
    def __init__(self, board, gameManager, parent = None):
        self.resultBoard = board
        self.children = []
        self.parent = parent
        if parent:
            self.alpha = parent.alpha
            self.beta = parent.beta
        else:
            self.alpha = -math.inf
            self.beta = math.inf
        self.gameManager = gameManager
        self.type = Type.Maximizer if self.gameManager.turnColor == PlayerColor.White else Type.Minimizer

    @staticmethod
    def createTree(board, depth, gameManager):
        root = BoardStateTree(board, gameManager, None)
        return root.createChildTrees(depth)

    def getBestMove(self):
        if self.type == Type.Maximizer:
            return max(self.children, key = lambda child: child.beta).move
        else:
            return min(self.children, key = lambda child: child.alpha).move

    def updateAlphaBeta(self, childTree):
        if self.type == Type.Maximizer:
            if childTree.beta > self.alpha:
                self.alpha = childTree.beta
        else:
            if childTree.alpha < self.beta:
                self.beta = childTree.alpha

    def shouldPrune(self):
        if self.beta <= self.alpha:
            return True
        return False

    def evaluatePosition(self):
        if self.gameManager.gameData.state == GameState.WhiteWon:
            return math.inf
        elif self.gameManager.gameData.state == GameState.BlackWon:
            return -math.inf
        elif self.gameManager.gameData.isDraw():
            return 0
        else:
            return Evaluator.evaluateBoard(self.resultBoard)

    def createChildTrees(self, depth):
        if depth == 0:
            boardValue = self.evaluatePosition()
            self.alpha = boardValue
            self.beta = boardValue
            return self

        allMoves = self.gameManager.getAllAvailableMoves()

        for move in allMoves:
            childNode = self.createChildNode(move, self.resultBoard)
            childTree = childNode.createChildTrees(depth - 1)
            self.updateAlphaBeta(childTree)
            self.children.append(childTree)

            if self.shouldPrune():
                break

        return self

    def createChildNode(self, move, board):
        virtualBoard = virtualizer.createVirtualBoard(board)

        virtualMove = move.switchBoard(board, virtualBoard)
        virtualGameManager = virtualizer.createVirtualGameManager(self.gameManager, virtualBoard)
        virtualGameManager.move(virtualMove)

        childStateTree = BoardStateTree(virtualBoard, virtualGameManager, self)
        childStateTree.move = move
        return childStateTree