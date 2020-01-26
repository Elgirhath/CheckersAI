import pygame, sys
from board import Board
from button_controller import ButtonController
from game_controller import GameController

screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

board = Board()
gameController = GameController(board)
while True:
    screen.fill((0,0,0))
    ButtonController.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    gameController.update()

    board.display(screen)
    pygame.display.flip()
    clock.tick(60)