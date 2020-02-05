from player_color import PlayerColor
from pawn import Pawn
from queen import Queen
from game_data import GameData, GameState

class GameManager:
    def __init__(self, board, turnColor = PlayerColor.White):
        self.board = board
        self.pieceToMove = None
        self.turnColor = turnColor
        self.whiteController = None
        self.blackController = None
        self.gameData = GameData()

    def setControllers(self, whiteController, blackController):
        self.whiteController = whiteController
        self.blackController = blackController

    def hasLost(self):
        if self.pieceToMove:
            return False # we might have no move right now, but turn goes to opposite player, so we haven't lost yet

        for piece in self.board.getArmy(self.turnColor):
            if piece.getPossibleMoves(self.board):
                return False
        return True

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

    def updateGameState(self):
        if self.gameData.isDraw():
            self.gameData.state = GameState.Draw
            return
        if len(self.getAllAvailableMoves()) == 0:
            if not self.pieceToMove:
                self.gameData.state = GameState.WhiteWon if self.turnColor == PlayerColor.Black else GameState.BlackWon
                return

    def update(self):
        if self.gameData.state != GameState.InProgress:
            return

        if len(self.getAllAvailableMoves()) == 0:
            if self.pieceToMove:
                self.changeTurn()
                return

        currentController = self.whiteController if self.turnColor == PlayerColor.White else self.blackController
        move = currentController.getMove()
        if move:
            self.executeMove(move)

    def promotePawn(self, pawn):
        pawn.square.piece = Queen(pawn.color, pawn.square)
        pawn.square = None

    def shouldBePromoted(self, piece):
        if self.board.getSquarePosition(piece.square)[0] == 7 and piece.color == PlayerColor.Black and type(piece) == Pawn:
            return True

        if self.board.getSquarePosition(piece.square)[0] == 0 and piece.color == PlayerColor.White and type(piece) == Pawn:
            return True
        return False

    def executeMove(self, move):
        self.gameData.addMove(self.turnColor, type(move.piece), move.toNumericalExpression(self.board))
        move.execute()

        grantNextMove = False
        promoted = False
        if self.shouldBePromoted(move.piece):
            self.promotePawn(move.piece)
            promoted = True

        if move.killedPiece and not promoted:
            grantNextMove = True
            self.pieceToMove = move.piece
            if not self.getAllAvailableMoves():
                grantNextMove = False
                self.pieceToMove = None

        if not grantNextMove:
            self.changeTurn()

        self.updateGameState()

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
        self.turnColor = PlayerColor.White if self.turnColor == PlayerColor.Black else PlayerColor.Black
