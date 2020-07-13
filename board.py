from pawn import Pawn
from player_color import PlayerColor
from board_square import BoardSquare

class Board():
    def getSquareColor(self, row, col):
        if (row + col) % 2:
            return PlayerColor.Black
        return PlayerColor.White
    
    def setupPawns(self):
        for row in range(3):
            for col in range(8):
                if self.getSquareColor(row, col) == PlayerColor.Black:
                    square = self.squares[row][col]
                    square.piece = Pawn(PlayerColor.Black, square)
                    
        for row in range(5,8):
            for col in range(8):
                if self.getSquareColor(row, col) == PlayerColor.Black:
                    square = self.squares[row][col]
                    square.piece = Pawn(PlayerColor.White, square)
    
    def setupBoard(self):
        for row in range(self.size):
            for col in range(self.size):
                self.squares[row][col] = BoardSquare(self.getSquareColor(row, col), (col, row), self.blockSize)

    def __init__(self):
        self.size = 8
        self.squares = [[[None] for x in range(self.size)] for y in range(self.size)]

        self.blockSize = 80

        self.setupBoard()

    def setupUI(self):
        for row in range(self.size):
            for col in range(self.size):
                self.squares[row][col].makeButton()

    def display(self, screen):
        for row in range(self.size):
            for col in range(self.size):
                square = self.squares[row][col]
                square.display(screen)

    def getSquarePosition(self, square):
        return (square.pos[1], square.pos[0])

    def getArmy(self, color):
        pieces = []
        for row in self.squares:
            for square in row:
                if square.piece and square.piece.color == color:
                    pieces.append(square.piece)

        return pieces