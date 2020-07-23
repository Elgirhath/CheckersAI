import unittest

from checkers.piece.pawn import Pawn
from checkers.piece.queen import Queen
from checkers.piece.piece import Piece
from checkers.board.board import Board
from checkers.board.board_builder import BoardBuilder
from checkers.game_manager import GameManager
from checkers.player_color import PlayerColor
from controllers.ai_controller import AiController
from ai.smart_evaluator import SmartEvaluator
from checkers.game_data import GameState
from debug import board_display

import pygame
import sys
import time

timePerMove = 1.
IN_DEBUG = False

class Tests(unittest.TestCase):
    def test_sacrifice_queen_to_win(self):
        board = Board()
        boardBuilder = BoardBuilder(board)
        white = [
            (Pawn, 2, 7),
            (Queen, 4, 7),
            (Queen, 3, 0)
        ]
        black = [
            (Queen, 7, 0)
        ]
        boardBuilder.build(boardBuilder.convertToSettings(white, black))
        
        gameManager = GameManager(board)

        player1 = AiController(board, gameManager, PlayerColor.White, SmartEvaluator(20), 4)
        player2 = AiController(board, gameManager, PlayerColor.Black, SmartEvaluator(20), 4)
        
        gameManager.setControllers(player1, player2)

        self.simulateGame(gameManager)

        self.assertEqual(len(gameManager.gameData.moves), 3)
        self.assertEqual(gameManager.gameData.state, GameState.WhiteWon)

    def test_promote_if_possible(self):
        board = Board()
        boardBuilder = BoardBuilder(board)
        white = [
            (Pawn, 7, 1),
            (Pawn, 6, 0),
            (Pawn, 5, 3),
            (Pawn, 5, 5),
            (Pawn, 1, 3)
        ]
        black = [
            (Pawn, 2, 0),
            (Pawn, 3, 5),
            (Pawn, 0, 6)
        ]
        boardBuilder.build(boardBuilder.convertToSettings(white, black))
        
        gameManager = GameManager(board)

        player1 = AiController(board, gameManager, PlayerColor.White, SmartEvaluator(20), 4)
        player2 = AiController(board, gameManager, PlayerColor.Black, SmartEvaluator(20), 4)
        
        gameManager.setControllers(player1, player2)

        gameManager.update()

        firstWhiteMove = gameManager.gameData.moves[0]

        self.assertEqual(firstWhiteMove.destPos[0], 0) # white promotes a pawn

    def simulateGame(self, gameManager):
        board = gameManager.board
        
        screen = None
        if IN_DEBUG:
            screen = pygame.display.set_mode((board.size * board.blockSize, board.size * board.blockSize))

        while True:
            self.update(gameManager, screen)

            gameState = gameManager.gameData.state
            if gameState and gameState != GameState.InProgress:
                return gameManager.gameData

    def update(self, gameManager, screen = None):
        if IN_DEBUG:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

            moveStartedTimestamp = time.time()

            gameManager.update()

            deltaTime = time.time() - moveStartedTimestamp
            timeToSleep = max(timePerMove - deltaTime, 0)
            time.sleep(timeToSleep)
            
            screen.fill((0, 0, 0))
            gameManager.board.display(screen)
            pygame.display.flip()
            clock = pygame.time.Clock()
            clock.tick(60)

        else:
            gameManager.update()

    @staticmethod
    def runTests(debug = False):
        global IN_DEBUG
        IN_DEBUG = debug
        sys.argv = [sys.argv[0]] # clean arguments to avoid collisions with unittests' arguments
        try:
            unittest.main()
        except SystemExit as se:
            pass