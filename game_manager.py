import numpy as np
from player_color import PlayerColor
from button_controller import ButtonController
from pawn import Pawn
from queen import Queen

class GameManager:
    turnColor = PlayerColor.white
    waitingForMove = True

    def __init__(self, board):
        self.board = board
        self.pieceToMove = None

    def setControllers(self, whiteController, blackController):
        self.whiteController = whiteController
        self.blackController = blackController

    def getAllAvailableMoves(self):
        needToKill = False
        allAvailableMoves = []

        if self.pieceToMove:
            needToKill = True
            allAvailableMoves = self.pieceToMove.getPossibleMoves(self.board)
        else:
            for piece in self.board.getArmy(self.turnColor):
                for move in piece.getPossibleMoves(self.board):
                    allAvailableMoves.append(move)
                    if move.killedPiece:
                        needToKill = True

        if needToKill:
            allAvailableMoves = list(move for move in allAvailableMoves if move.killedPiece != None)

        return allAvailableMoves

    def getPieceAvailableMoves(self, piece):
        allAvailableMoves = self.getAllAvailableMoves()
        currentPieceAvailableMoves = piece.getPossibleMoves(self.board)
        return list(move for move in currentPieceAvailableMoves if move in allAvailableMoves)

    def update(self):
        currentController = self.whiteController if self.turnColor == PlayerColor.white else self.blackController
        if len(self.getAllAvailableMoves()) == 0:
            if self.pieceToMove:
                self.changeTurn()
            else:
                return PlayerColor.black if self.turnColor == PlayerColor.white else PlayerColor.white
        move = currentController.getMove()
        if move:
            self.move(move)
        return None

    def promotePawn(self, pawn):
        pawn.square.piece = Queen(pawn.color, pawn.square)
        pawn.square = None

    def shouldBePromoted(self, piece):
        if self.board.getSquarePosition(piece.square)[0] == 7 and piece.color == PlayerColor.black and type(piece) == Pawn:
            return True
            
        if self.board.getSquarePosition(piece.square)[0] == 0 and piece.color == PlayerColor.white and type(piece) == Pawn:
            return True

    def move(self, move):
        grantNextMove = False

        move.execute()

        promoted = False
        if self.shouldBePromoted(move.piece):
            self.promotePawn(move.piece)
            promoted = True

        if move.killedPiece and not promoted:
            grantNextMove = True
            self.pieceToMove = move.piece

        if not grantNextMove:
            self.changeTurn()

    def deselect(self):
        for square in self.board.getSquareList():
            square.selected = False

    def clearPossibleMoves(self):
        for square in self.board.getSquareList():
            square.isPossibleMove = False

    def changeTurn(self):
        self.pieceToMove = None
        self.clearPossibleMoves()
        self.deselect()
        self.turnColor = PlayerColor.white if self.turnColor == PlayerColor.black else PlayerColor.black