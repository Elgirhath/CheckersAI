import pygame
import sys

from controllers.ai_controller import AiController
from controllers.player_controller import PlayerController
from board import Board
from board_builder import BoardBuilder
from button_controller import ButtonController
from game_manager import GameManager
from player_color import PlayerColor
from tests import e2e_tests as tests
from game_data import GameState
import ai.create_database

board = Board()
board.setupPawns()

screen = pygame.display.set_mode((board.size * board.blockSize, board.size * board.blockSize))
clock = pygame.time.Clock()

board.setupUI()
boardBuilder = BoardBuilder(board)
# tests.trap_a_queen(boardBuilder)
gameManager = GameManager(board)

player1 = PlayerController(board, gameManager, PlayerColor.White)
# player1 = AiController(board, gameManager, PlayerColor.White)
# player2 = PlayerController(board, gameManager, PlayerColor.Black)
player2 = AiController(board, gameManager, PlayerColor.Black)

gameManager.setControllers(player1, player2)

while True:
    screen.fill((0, 0, 0))
    ButtonController.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    gameManager.update()
    gameState = gameManager.gameData.state
    if gameState and gameState != GameState.InProgress:
        print(gameManager.gameData.state)
        sys.exit(0)

    board.display(screen)
    pygame.display.flip()
    clock.tick(60)