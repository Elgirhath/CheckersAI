from piece import Piece
from move import Move
import pygame
from player_color import PlayerColor

whiteIcon = './graphics/white_queen.png'
blackIcon = './graphics/black_queen.png'

class Queen(Piece):
    def __init__(self, color, square):
        super().__init__(color, square)
        self.icon = pygame.image.load(whiteIcon if color == PlayerColor.White else blackIcon)

    def getPossibleMoves(self, board):
        (row, col) = board.getSquarePosition(self.square)
        
        possibleMoves = []

        movesToCheck = set()
        for i in range(0, 8):
            movesToCheck.add((row - i, col - i))
            movesToCheck.add((row + i, col - i))
            movesToCheck.add((row + i, col + i))
            movesToCheck.add((row - i, col + i))

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
        distance = abs(row - currentPos[0])
        if distance > 1:
            sign = lambda x: (1, -1)[x<0]
            jumpedPieceRow = row - sign(row - currentPos[0])
            jumpedPieceCol = col - sign(col - currentPos[1])
            jumpedPiece = board.squares[jumpedPieceRow, jumpedPieceCol].piece

            for i in range(1, distance - 1):
                rowToCheck = currentPos[0] + sign(row - currentPos[0]) * i
                colToCheck = currentPos[1] + sign(col - currentPos[1]) * i
                if board.squares[rowToCheck, colToCheck].piece:
                    return None

            if jumpedPiece:
                if jumpedPiece.color == self.color:
                    return None
                killed = jumpedPiece

        return Move(self, board.squares[row, col], killed)