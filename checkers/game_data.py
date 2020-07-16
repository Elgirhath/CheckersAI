from enum import Enum
from checkers.player_color import PlayerColor
from checkers.piece.queen import Queen
from checkers import game_settings

class GameState(Enum):
    InProgress = 0
    WhiteWon = 1
    Draw = 2
    BlackWon = 3

class MoveRecord:
    def __init__(self, color, pieceType, sourcePos, destPos, killedPos):
        self.color = color
        self.pieceType = pieceType
        self.sourcePos = sourcePos
        self.destPos = destPos
        self.killedPos = killedPos

class GameData:
    def __init__(self):
        self.moves = []
        self.hasEnded = False
        self.state = GameState.InProgress

    def addMove(self, color, pieceType, move):
        sourcePos, destPos, killedPos = move
        self.moves.append(MoveRecord(color, pieceType, sourcePos, destPos, killedPos))
        self.cleanOverhead()

    def cleanOverhead(self):
        move_overhead = len(self.moves) - game_settings.moves_to_keep
        if move_overhead > 0:
            del self.moves[0 : move_overhead]

    def getMovesOf(self, player_color):
        return list(move for move in self.moves if move.color == player_color)

    def isDraw(self):
        blackMoves = self.getMovesOf(PlayerColor.Black)
        if len(blackMoves) < game_settings.move_repeat_to_draw * 2: # game is shorter than required moves to draw
            return False

        lastBlackMoves = list((move.sourcePos, move.destPos, move.killedPos) for move in blackMoves[-game_settings.move_repeat_to_draw:])

        if any(killed for _, _, killed in lastBlackMoves if killed is not None): # any piece was taken in last black moves
            return False

        whiteMoves = self.getMovesOf(PlayerColor.White)
        if len(whiteMoves) < game_settings.move_repeat_to_draw * 2:
            return False

        lastWhiteMoves = list((move.sourcePos, move.destPos, move.killedPos) for move in whiteMoves[-game_settings.move_repeat_to_draw:])

        if any(killed for _, _, killed in lastWhiteMoves if killed is not None):
            return False

        if len(set(lastBlackMoves)) == 2 and len(set(lastWhiteMoves)) == 2:
            return True

        if len(self.moves) < game_settings.queen_repeat_to_draw:
            return False

        lastMovesToCheckQueens = self.moves[-game_settings.queen_repeat_to_draw:]
        if all(move.pieceType == Queen for move in lastMovesToCheckQueens if move.killedPos is None):
            return True

        return False