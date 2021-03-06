from checkers.player_color import PlayerColor
from checkers.piece.pawn import Pawn
from checkers.piece.queen import Queen
from checkers.game_manager import GameManager
from ai.virtualizer import *
from checkers.move import Move

class FeatureExtractor:
    def __init__(self, gameManager):
        virtualBoard = createVirtualBoard(gameManager.board)
        self.gameManager = createVirtualGameManager(gameManager, virtualBoard)
        self.army = {
            PlayerColor.White: [],
            PlayerColor.Black: []
        }

    def getFeatures(self):
        self.updateMemo()
        board = self.gameManager.board
        return [
            self.getPieceCount(PlayerColor.White),
            self.getPieceCount(PlayerColor.Black),
            self.getPieceCount(PlayerColor.White, Pawn),
            self.getPieceCount(PlayerColor.Black, Pawn),
            self.getPieceCount(PlayerColor.White, Queen),
            self.getPieceCount(PlayerColor.Black, Queen),
            # self.getPossibleMovesCount(PlayerColor.White),
            # self.getPossibleMovesCount(PlayerColor.Black),
            # self.getAveragePawnAdvance(PlayerColor.White),
            # self.getAveragePawnAdvance(PlayerColor.Black),
            self.getPiecesOnEdge(PlayerColor.White),
            self.getPiecesOnEdge(PlayerColor.Black)
            ]

    def updateMemo(self):
        board = self.gameManager.board
        self.army[PlayerColor.White] = board.getArmy(PlayerColor.White)
        self.army[PlayerColor.Black] = board.getArmy(PlayerColor.Black)

    def getAveragePawnAdvance(self, color):
        board = self.gameManager.board
        army = self.army[color]
        sum = 0.0
        for piece in army:
            sum += board.getSquarePosition(piece.square)[0]
        
        if len(army) == 0:
            return 0
            
        avg = sum / len(army)
        if color == PlayerColor.White:
            avg = float(board.size - 1) - avg
        return avg

    def getPossibleMovesCount(self, color):
        board = self.gameManager.board
        army = self.army[color]
        sum = 0
        for piece in army:
            sum += len(piece.getPossibleMoves(board))
        return sum

    def getPieceCount(self, color, pieceType = None):
        board = self.gameManager.board
        return len(list(piece for piece in self.army[color] if pieceType is None or type(piece) == pieceType))
        
    def getPiecesOnEdge(self, color):
        board = self.gameManager.board
        i = 0
        for piece in self.army[color]:
            piecePosition = board.getSquarePosition(piece.square)
            if piecePosition[1] == 0 or piecePosition[1] == board.size - 1:
                i += 1
        return i
        
    @staticmethod
    def extractFeaturesFromGameData(gameData):
        moveRecords = gameData.moves
        
        board = Board()
        board.setupPawns()
        gameManager = GameManager(board)

        states = []

        for moveRecord in moveRecords:
            moveNumerical = (moveRecord.sourcePos, moveRecord.destPos, moveRecord.killedPos)
            move = Move.fromNumericalExpression(moveNumerical, gameManager.board)
            gameManager.executeMove(move)
            
            featureExtractor = FeatureExtractor(gameManager)
            states.append(featureExtractor.getFeatures())

        return states