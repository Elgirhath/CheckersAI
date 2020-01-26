from pawn import Pawn
from queen import Queen
from board import Board
from player_color import PlayerColor

white = PlayerColor.white
black = PlayerColor.black

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

    def setup(self):
        white = [
            (Pawn, 1, 1),
            (Queen, 5, 3)
        ]
        black = [
            (Pawn, 6, 6),
            (Queen, 0, 6)
        ]
        self.build(self.convertToSettings(white, black))

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