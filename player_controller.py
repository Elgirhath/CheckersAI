from button_controller import ButtonController

class PlayerController():
    def __init__(self, board, gameManager, color):
        self.board = board
        self.gameManager = gameManager
        self.color = color
        self.possibleMoves = []
        self.selectedSquare = None
        
    def select(self, square):
        for _square in self.board.getSquareList():
            _square.selected = False
        square.selected = True


    def displayPossibleMoves(self):
        self.gameManager.clearPossibleMoves()

        for move in self.possibleMoves:
            move.destSquare.isPossibleMove = True

    def getMoveByDest(self, square):
        for move in self.possibleMoves:
            if move.destSquare == square:
                return move
        return None

    def toggleSelect(self, square):
        if square.selected:
            self.gameManager.clearPossibleMoves()
            self.gameManager.deselect()
            self.selectedSquare = None
        else:
            self.select(square)
            self.selectedSquare = square
        
    def getPressedSquare(self):
        squareList = self.board.getSquareList()
        pressedButtons = ButtonController.getPressed()
        for square in squareList:
            if square.button in pressedButtons:
                if square.isPossibleMove:
                    return square
                if not square.piece:
                    continue
                if square.piece.color != self.gameManager.turnColor:
                    continue
                return square

    def getMove(self):
        pressedSquare = self.getPressedSquare()
        if pressedSquare:
            if pressedSquare.piece and pressedSquare.piece.color == self.color:
                self.toggleSelect(pressedSquare)

            if self.selectedSquare:
                if pressedSquare != self.selectedSquare:
                    move = self.getMoveByDest(pressedSquare)
                    if move:
                        self.gameManager.clearPossibleMoves()
                        self.gameManager.deselect()
                        self.selectedSquare = None
                        return move

                self.possibleMoves = self.gameManager.getPieceAvailableMoves(self.selectedSquare.piece)
                self.displayPossibleMoves()