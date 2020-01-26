import pygame, sys
from board import Board
from button_controller import ButtonController
from game_manager import GameManager
from player_controller import PlayerController
from ai_controller import AiController
from player_color import PlayerColor
from board_builder import BoardBuilder

screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

board = Board()
boardBuilder = BoardBuilder(board)
# boardBuilder.setup()
gameManager = GameManager(board)

player1 = PlayerController(board, gameManager, PlayerColor.white)
player2 = PlayerController(board, gameManager, PlayerColor.black)
# player2 = AiController(board, gameManager, PlayerColor.black)

gameManager.setControllers(player1, player2)

while True:
    screen.fill((0,0,0))
    ButtonController.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    gameResult = gameManager.update()
    if gameResult:
        print(gameResult)
        sys.exit(0)

    board.display(screen)
    pygame.display.flip()
    clock.tick(60)