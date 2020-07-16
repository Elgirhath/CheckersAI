import pygame
import sys

from controllers.ai_controller import AiController
from controllers.player_controller import PlayerController
from checkers.board.board import Board
from checkers.board.board_builder import BoardBuilder
from checkers.board.button_controller import ButtonController
from checkers.game_manager import GameManager
from checkers.player_color import PlayerColor
from tests import e2e_tests as tests
from checkers.game_data import GameState
from ai.game_simulator import GameSimulator
from ai.smart_evaluator import SmartEvaluator
import checkers.debug

board = Board()
board.setupPawns()

screen = pygame.display.set_mode((board.size * board.blockSize, board.size * board.blockSize))
clock = pygame.time.Clock()

board.setupUI()
boardBuilder = BoardBuilder(board)
# tests.sack_queen_to_win(boardBuilder)
gameManager = GameManager(board)

# player1 = PlayerController(board, gameManager, PlayerColor.White)
player1 = AiController(board, gameManager, PlayerColor.White, SmartEvaluator(2), 4)
# player2 = PlayerController(board, gameManager, PlayerColor.Black)
player2 = AiController(board, gameManager, PlayerColor.Black, SmartEvaluator(2), 4)

gameManager.setControllers(player1, player2)
board.display(screen)
pygame.display.flip()

while True:
    ButtonController.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    gameManager.update()
    gameState = gameManager.gameData.state
    if gameState and gameState != GameState.InProgress:
        print(gameManager.gameData.state)
        sys.exit(0)

    screen.fill((0, 0, 0))
    board.display(screen)
    pygame.display.flip()
    clock.tick(60)