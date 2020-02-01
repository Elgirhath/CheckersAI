class Move:
    def __init__(self, piece = None, destSquare = None, killedPiece = None):
        self.piece = piece
        self.destSquare = destSquare
        self.killedPiece = killedPiece

    def execute(self):
        if self.killedPiece:
            self.killedPiece.kill()
        self.piece.move(self.destSquare)

    def __eq__(self, other):
        return self.piece == other.piece and self.destSquare == other.destSquare and self.killedPiece == other.killedPiece

    def toNumericalExpression(self, board):
        piecePosition = board.getSquarePosition(self.piece.square)
        destSquarePosition = board.getSquarePosition(self.destSquare)
        killedPiecePosition = board.getSquarePosition(self.killedPiece.square) if self.killedPiece else None
        return (piecePosition, destSquarePosition, killedPiecePosition)

    @staticmethod
    def fromNumericalExpression(numerical, board):
        (piecePos, desSquarePos, killedPiecePos) = numerical
        piece = board.squares[piecePos[0], piecePos[1]].piece
        destSquare = board.squares[desSquarePos[0], desSquarePos[1]]
        killedPiece = board.squares[killedPiecePos[0], killedPiecePos[1]].piece if killedPiecePos else None
        return Move(piece, destSquare, killedPiece)

    def switchBoard(self, srcBoard, destBoard):
        numericalMove = self.toNumericalExpression(srcBoard)
        return Move.fromNumericalExpression(numericalMove, destBoard)