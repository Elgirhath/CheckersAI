from checkers.player_color import PlayerColor
import pygame
from checkers.board.button import Button

whiteSquareColor = (255, 255, 255)
blackSquareColor = (181, 136, 99)
selectedWhiteColor = (200, 200, 200)
selectedBlackColor = (100, 70, 50)

possibleMoveCircleColor = (120, 120, 120, 0)
possibleMoveCircleRadius = 20

class BoardSquare():
    def getColor(self):
        if self.playerColor == PlayerColor.Black and not self.selected:
            return blackSquareColor
        elif self.playerColor == PlayerColor.Black:
            return selectedBlackColor
        elif not self.selected:
            return whiteSquareColor
        else:
            return selectedWhiteColor

    def __init__(self, playerColor, pos, size):
        self.playerColor = playerColor
        self.selected = False
        self.isPossibleMove = False
        self.piece = None
        self.pos = pos
        self.size = size

    def makeButton(self):
        self.button = Button((self.pos[0] * self.size, self.pos[1] * self.size), (self.size, self.size))
        

    def display(self, screen):
        color = self.getColor()

        pixel_pos = (self.pos[0] * self.size, self.pos[1] * self.size)

        rect = pygame.Rect(pixel_pos[0], pixel_pos[1], pixel_pos[0] + self.size, pixel_pos[1] + self.size)
        pygame.draw.rect(screen, color, rect)
        if self.isPossibleMove:
            circleCenter = (int(pixel_pos[0] + (self.size / 2)), int(pixel_pos[1] + (self.size / 2)))
            pygame.draw.circle(screen, possibleMoveCircleColor, circleCenter, possibleMoveCircleRadius)
        if self.piece:
            self.piece.display(screen, pixel_pos, (self.size, self.size))