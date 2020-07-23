from checkers.board.board import Board
from checkers.board.board_builder import BoardBuilder
from checkers.game_manager import GameManager
import copy

def createVirtualBoard(board):
    virtualBoard = Board()
    BoardBuilder(virtualBoard).copy(board)
    return virtualBoard

def createVirtualGameManager(gameManager, virtualBoard):
    nextTurnColor = gameManager.turnColor
    virtualGameManager = GameManager(virtualBoard, nextTurnColor)
    virtualGameManager.pieceToMove = gameManager.pieceToMove
    virtualGameManager.gameData = copy.deepcopy(gameManager.gameData)
    return virtualGameManager