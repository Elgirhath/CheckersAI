from controllers.ai_controller import AiController
from controllers.random_controller import RandomController
from checkers.board.board import Board
from checkers.game_manager import GameManager
from checkers.player_color import PlayerColor
from checkers.game_data import GameState
import pygame
from ai.utils import addRows
import sys
from itertools import chain
from ai.feature_extractor import FeatureExtractor
from ai.static_evaluator import StaticEvaluator

class GameSimulator:
    def getResultLabels(self, gameState):
        if gameState == GameState.Draw:
            return [0,0,1]
        if gameState == GameState.WhiteWon:
            return [1,0,0]
        if gameState == GameState.BlackWon:
            return [0,1,0]

    def simulateGame(self, randomMoveNumber, use_gui = False):
        clock = pygame.time.Clock()
        board = Board()
        board.setupPawns()
        gameManager = GameManager(board)

        evaluator = StaticEvaluator()
        player1 = AiController(board, gameManager, PlayerColor.White, evaluator=evaluator)
        player2 = AiController(board, gameManager, PlayerColor.Black, evaluator=evaluator)

        random1 = RandomController(board, gameManager, PlayerColor.White)
        random2 = RandomController(board, gameManager, PlayerColor.Black)

        gameManager.setControllers(random1, random2)

        if use_gui:
            board.setupUI()
            screen = pygame.display.set_mode((board.size * board.blockSize, board.size * board.blockSize))

        while True:
            gameManager.update()
            gameState = gameManager.gameData.state
            randomMoveNumber -= 1
            if randomMoveNumber == 0:
                gameManager.setControllers(player1, player2)

            if gameState != GameState.InProgress:
                return gameManager.gameData

            if use_gui:
                screen.fill((0, 0, 0))
                board.display(screen)
                pygame.display.flip()
                clock.tick(60)

    def simulateAndSave(self, gamesToPlay, file_path):
        records_to_save = []

        randomMoveTotal = 6

        for i in range(gamesToPlay):
            progressBarLength = 50
            fill = int(i/gamesToPlay * progressBarLength)
            sys.stdout.write(f"\rGames processed: {i}/{gamesToPlay} [{'='*fill}>{'.'*(progressBarLength - fill - 1)}]")

            gameData = self.simulateGame(randomMoveTotal, True)
            states = FeatureExtractor.extractFeaturesFromGameData(gameData)
            labels = self.getResultLabels(gameData.state)

            records_to_save.extend(list(chain(features + labels for features in states)))

        sys.stdout.write(f"\rGames processed: {gamesToPlay}/{gamesToPlay} [{'='*progressBarLength}]\n")
        
        addRows(records_to_save, file_path)