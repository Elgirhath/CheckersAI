from player_color import PlayerColor
import pygame
from button import Button

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
        self.button = Button(self.pos, self.size)
        

    def display(self, screen):
        color = self.getColor()

        rect = pygame.Rect(self.pos[0], self.pos[1], self.pos[0] + self.size[0], self.pos[1] + self.size[1])
        pygame.draw.rect(screen, color, rect)
        if self.isPossibleMove:
            circleCenter = (int(self.pos[0] + (self.size[0] / 2)), int(self.pos[1] + (self.size[1] / 2)))
            pygame.draw.circle(screen, possibleMoveCircleColor, circleCenter, possibleMoveCircleRadius)
        if self.piece:
            self.piece.display(screen, self.pos, self.size)