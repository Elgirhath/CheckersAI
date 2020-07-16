from checkers.player_color import PlayerColor
import abc
import pygame

class Piece():
    __metaclass__ = abc.ABCMeta

    def __init__(self, color, square):
        self.icon = None  # set in inherited
        self.selected = False
        self.color = color
        self.square = square

    def display(self, screen, _pos, _size):
        icon = pygame.transform.scale(self.icon, _size)
        screen.blit(icon, _pos)

    def kill(self):
        self.square.piece = None
        self.square = None

    def move(self, square):
        self.square.piece = None
        self.square = square
        square.piece = self

    @abc.abstractmethod
    def getPossibleMoves(self, board):
        return 

    def checkSquare(self, board, row, col):
        if row < 0 or row >= board.size:
            return False
        if col < 0 or col >= board.size:
            return False
        if board.squares[row][col].piece is not None:
            return False
        return True