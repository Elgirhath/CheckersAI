from player_color import PlayerColor
from pawn import Pawn
from queen import Queen
import copy

white = PlayerColor.White
black = PlayerColor.Black

class BoardBuilder:
    def __init__(self, board):
        self.board = board

    def build(self, settings):
        for square in self.board.getSquareList():
            if square.piece:
                square.piece.square = None
            square.piece = None

        for setting in settings:
            pieceClass = globals()[setting.type.__name__]
            square = self.board.squares[setting.row, setting.column]
            square.piece = pieceClass(setting.color, square)

    def copy(self, board):
        for i in range(self.board.size):
            for j in range(self.board.size):
                self.board.squares[i, j].piece = None
                copiedPiece = board.squares[i, j].piece
                if copiedPiece:
                    piece = self.board.squares[i, j].piece
                    piece = copy.copy(copiedPiece)
                    piece.square = self.board.squares[i, j]
                    self.board.squares[i, j].piece = piece


    def convertToSettings(self, whiteSettings, blackSettings):
        settings = []
        for setting in whiteSettings:
            settings.append(Setting(setting[0], setting[1], setting[2], white))
        for setting in blackSettings:
            settings.append(Setting(setting[0], setting[1], setting[2], black))

        return settings

class Setting:
    def __init__(self, type, row, column, color):
        self.type = type
        self.row = row
        self.column = column
        self.color = color