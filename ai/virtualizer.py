from board import Board
from board_builder import BoardBuilder
from game_manager import GameManager
import copy

def createVirtualBoard(board):
    virtualBoard = Board()
    BoardBuilder(virtualBoard).copy(board)
    return virtualBoard

def createVirtualGameManager(gameManager, virtualBoard):
    nextTurnColor = gameManager.turnColor
    virtualGameManager = GameManager(virtualBoard, nextTurnColor)
    virtualGameManager.pieceToMove = gameManager.pieceToMove
    virtualGameManager.gameData = copy.copy(gameManager.gameData)
    return virtualGameManager