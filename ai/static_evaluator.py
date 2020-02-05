from player_color import PlayerColor
from pawn import Pawn

class StaticEvaluator:
    def evaluateBoard(self, gameManager):
        board = gameManager.board
        whiteArmy = board.getArmy(PlayerColor.White)
        blackArmy = board.getArmy(PlayerColor.Black)

        sum = 0.
        for piece in whiteArmy:
            if type(piece) == Pawn:
                sum += 1.
            else:
                sum += 3.

            piecePos = board.getSquarePosition(piece.square)
            if piecePos[1] == 0 or piecePos[1] == board.size - 1:
                sum += 0.1
        
        for piece in blackArmy:
            if type(piece) == Pawn:
                sum -= 1.
            else:
                sum -= 3.
                
            piecePos = board.getSquarePosition(piece.square)
            if piecePos[1] == 0 or piecePos[1] == board.size - 1:
                sum -= 0.1

        return sum