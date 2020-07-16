from checkers.piece.piece import Piece
from checkers.player_color import PlayerColor
from checkers.move import Move
import pygame

whiteIcon = pygame.image.load('./graphics/white_pawn.png')
blackIcon = pygame.image.load('./graphics/black_pawn.png')

class Pawn(Piece):
    def __init__(self, color, square):
        super().__init__(color, square)
        self.icon = whiteIcon if color == PlayerColor.White else blackIcon

    def getPossibleMoves(self, board):
        (row, col) = board.getSquarePosition(self.square)
        
        possibleMoves = []

        if self.color == PlayerColor.White:
            movesToCheck = [(row - 1, col - 1), (row - 2, col - 2), (row - 1, col + 1), (row - 2, col + 2), (row + 2, col + 2), (row + 2, col - 2)]
        else:
            movesToCheck = [(row + 1, col + 1), (row + 2, col + 2), (row + 1, col - 1), (row + 2, col - 2), (row - 2, col + 2), (row - 2, col - 2)]

        for move in movesToCheck:
            potentialMove = self.getMove(board, move[0], move[1])
            if potentialMove:
                possibleMoves.append(potentialMove)

        return possibleMoves

    def getMove(self, board, row, col):
        if not self.checkSquare(board, row, col):
            return None
        
        currentPos = board.getSquarePosition(self.square)
        
        killed = None
        if abs(row - currentPos[0]) == 2:
            jumpedPiecePos = (int((row + currentPos[0])/2), int((col + currentPos[1])/2))
            jumpedPiece = board.squares[jumpedPiecePos[0]][jumpedPiecePos[1]].piece
            if not jumpedPiece:
                return None

            if jumpedPiece.color == self.color:
                if row - currentPos[0] > 0 and self.color == PlayerColor.White:
                    return None
                if row - currentPos[0] < 0 and self.color == PlayerColor.Black:
                    return None
            else:
                killed = jumpedPiece

        return Move(self, board.squares[row][col], killed)