import numpy as np
from numpy import matrix
from piece import Piece
from pawn import Pawn
from queen import Queen
from player_color import PlayerColor
from board_square import BoardSquare
import pygame

class Board():
    def getSquareColor(self, row, col):
        if (row + col) % 2:
            return PlayerColor.black
        return PlayerColor.white
    
    def setupPawns(self):
        for row in range(3):
            for col in range(8):
                if self.getSquareColor(row, col) == PlayerColor.white:
                    square = self.boardSquares[row, col]
                    square.piece = Pawn(PlayerColor.black, square)
                    
        for row in range(5,8):
            for col in range(8):
                if self.getSquareColor(row, col) == PlayerColor.white:
                    square = self.boardSquares[row, col]
                    square.piece = Pawn(PlayerColor.white, square)
    
    def setupBoard(self):
        for row in range(8):
            for col in range(8):
                pos = (col * self.blockSize, row * self.blockSize)
                size = (self.blockSize, self.blockSize)
                self.boardSquares[row, col] = BoardSquare(self.getSquareColor(row, col), pos, size)

    def __init__(self):
        self.boardSize = 8
        self.boardSquares = matrix([[None] * self.boardSize] * self.boardSize)

        self.blockSize = 100

        self.setupBoard()
        self.setupPawns()

    def display(self, screen):
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                square = self.boardSquares[row, col]
                square.display(screen)

    def getSquareList(self):
        return np.asarray(self.boardSquares).reshape(-1)

    def getSquarePosition(self, square):
        for pos, _square in np.ndenumerate(self.boardSquares):
            if _square == square:
                return pos

    def getArmy(self, color):
        return list(square.piece for square in self.getSquareList() if square.piece and square.piece.color == color)
