import pygame
import sys

from controllers.ai_controller import AiController
from controllers.player_controller import PlayerController
from checkers.board.board import Board
from checkers.board.board_builder import BoardBuilder
from checkers.board.button_controller import ButtonController
from checkers.game_manager import GameManager
from checkers.player_color import PlayerColor
from checkers.game_data import GameState
from ai.game_simulator import GameSimulator
from ai.smart_evaluator import SmartEvaluator
import argparse

def update():
    gameManager.update()

    gameState = gameManager.gameData.state
    
    if gameState and gameState != GameState.InProgress:
        print(gameManager.gameData.state)
        sys.exit(0)

parser = argparse.ArgumentParser(description='Run checkers')
parser.add_argument('-cc', action="store_true", help='computer vs computer')
parser.add_argument('-cp', action="store_true", help='computer vs player')
parser.add_argument('-pc', action="store_true", help='player vs computer')
parser.add_argument('-pp', action="store_true", help='player vs player')

args = parser.parse_args()

board = Board()
board.setupPawns()

screen = pygame.display.set_mode((board.size * board.blockSize, board.size * board.blockSize))
clock = pygame.time.Clock()

board.setupButtons()
gameManager = GameManager(board)

if args.cc:
    player1 = AiController(board, gameManager, PlayerColor.White, SmartEvaluator(50), 4)
    player2 = AiController(board, gameManager, PlayerColor.Black, SmartEvaluator(50), 4)

if args.cp:
    player1 = AiController(board, gameManager, PlayerColor.White, SmartEvaluator(50), 4)
    player2 = PlayerController(board, gameManager, PlayerColor.Black)

if args.pc:
    player1 = PlayerController(board, gameManager, PlayerColor.White)
    player2 = AiController(board, gameManager, PlayerColor.Black, SmartEvaluator(50), 4)

if args.pp:
    player1 = PlayerController(board, gameManager, PlayerColor.White)
    player2 = PlayerController(board, gameManager, PlayerColor.Black)

gameManager.setControllers(player1, player2)
board.display(screen)
pygame.display.flip()

while True:
    ButtonController.updatePressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    update()

    screen.fill((0, 0, 0))
    board.display(screen)
    pygame.display.flip()
    clock.tick(60)