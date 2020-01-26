import numpy as np
from player_color import PlayerColor
from button_controller import ButtonController
from pawn import Pawn
from queen import Queen

class GameController:
    turnColor = PlayerColor.white
    waitingForMove = True

    def __init__(self, board):
        self.board = board
        self.possibleMoves = []
        self.pieceToMove = None

    def getSelected(self):
        for square in self.board.getSquareList():
            if square.selected:
                return square
        return None
    
    def processInput(self):
        squareList = self.board.getSquareList()
        pressedButtons = ButtonController.getPressed()
        for square in squareList:
            if square.button in pressedButtons:
                if square.isPossibleMove:
                    return square
                if not square.piece:
                    continue
                if square.piece.color != self.turnColor:
                    continue
                return square

    def select(self, square):
        for _square in self.board.getSquareList():
            _square.selected = False
        square.selected = True

    def deselect(self):
        for square in self.board.getSquareList():
            square.selected = False

    def clearPossibleMoves(self):
        for square in self.board.getSquareList():
            square.isPossibleMove = False

    def getMoveByDest(self, square):
        for move in self.possibleMoves:
            if move.destSquare == square:
                return move
        return None

    def displayPossibleMoves(self):
        self.clearPossibleMoves()

        for move in self.possibleMoves:
            move.destSquare.isPossibleMove = True

    def toggleSelect(self, square):
        if square.selected:
            self.clearPossibleMoves()
            self.deselect()
        else:
            self.select(square)

    def update(self):
        allAvailableMoves = self.getFilteredMoves()
        if len(allAvailableMoves) == 0:
            if self.pieceToMove == None:
                print("Player %s won!" %(PlayerColor.black if self.turnColor == PlayerColor.white else PlayerColor.white) )
                return
            self.changeTurn()
            return
        selectedSquare = self.processInput()
        if selectedSquare:
            if selectedSquare.piece and selectedSquare.piece.color == self.turnColor:
                self.toggleSelect(selectedSquare)

            move = self.getMoveByDest(selectedSquare)
            if move:
                self.move(move)
                return
                
            if self.getSelected():
                currentPieceAvailableMoves = self.getSelected().piece.getPossibleMoves(self.board)
                self.possibleMoves = list(move for move in currentPieceAvailableMoves if move in allAvailableMoves)
                self.displayPossibleMoves()

    def getFilteredMoves(self):
        needToKill = False
        filteredMoves = []

        if self.pieceToMove:
            needToKill = True
            filteredMoves = self.pieceToMove.getPossibleMoves(self.board)
        else:
            for piece in self.board.getArmy(self.turnColor):
                for move in piece.getPossibleMoves(self.board):
                    filteredMoves.append(move)
                    if move.killedPiece:
                        needToKill = True

        if needToKill:
            filteredMoves = list(move for move in filteredMoves if move.killedPiece != None)

        return filteredMoves

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
        else:
            self.clearPossibleMoves()
            self.deselect()
            
        self.possibleMoves = []

    def changeTurn(self):
        self.pieceToMove = None
        self.clearPossibleMoves()
        self.deselect()
        self.turnColor = PlayerColor.white if self.turnColor == PlayerColor.black else PlayerColor.black