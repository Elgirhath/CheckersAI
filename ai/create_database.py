from controllers.ai_controller import AiController
from controllers.random_controller import RandomController
from board import Board
from game_manager import GameManager
from player_color import PlayerColor
from game_data import GameState
import pygame


file = []

clock = pygame.time.Clock()

i = 10
randomMoveTotal = 6

while i > 0:
    board = Board()
    board.setupPawns()
    gameManager = GameManager(board)

    player1 = AiController(board, gameManager, PlayerColor.White)
    player2 = AiController(board, gameManager, PlayerColor.Black)

    random1 = RandomController(board, gameManager, PlayerColor.White)
    random2 = RandomController(board, gameManager, PlayerColor.Black)

    gameManager.setControllers(random1, random2)

    board.setupUI()
    screen = pygame.display.set_mode((board.size * board.blockSize, board.size * board.blockSize))

    while True:
        screen.fill((0, 0, 0))

        gameManager.update()
        gameState = gameManager.gameData.state
        randomMoveTotal -= 1
        if randomMoveTotal <= 0:
            gameManager.setControllers(player1, player2)

        if gameState != GameState.InProgress:
            print(gameState)
            if gameState == GameState.Draw:
                value = 0
            elif gameState == GameState.WhiteWon:
                value = 1
            elif gameState == GameState.BlackWon:
                value = -1
            file.append(value)
            i -= 1
            break

        board.display(screen)
        pygame.display.flip()
        clock.tick(60)

print(file)