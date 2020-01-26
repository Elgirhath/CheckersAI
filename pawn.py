from piece import Piece
from player_color import PlayerColor
from move import Move
import pygame

whiteIcon = './graphics/white_pawn.png'
blackIcon = './graphics/black_pawn.png'

class Pawn(Piece):
    def __init__(self, color, square):
        super().__init__(color, square)
        self.icon = pygame.image.load(whiteIcon if color == PlayerColor.white else blackIcon)

    def getPossibleMoves(self, board):
        (row, col) = board.getSquarePosition(self.square)
        
        possibleMoves = []

        if self.color == PlayerColor.white:
            movesToCheck = [(row - 1, col - 1), (row - 2, col - 2), (row - 1, col + 1), (row - 2, col + 2)]
        else:
            movesToCheck = [(row + 1, col + 1), (row + 2, col + 2), (row + 1, col - 1), (row + 2, col - 2)]

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
            jumpedPiece = board.boardSquares[jumpedPiecePos[0], jumpedPiecePos[1]].piece
            if not jumpedPiece:
                return None
            if jumpedPiece.color != self.color:
                killed = jumpedPiece

        return Move(self, board.boardSquares[row, col], killed)