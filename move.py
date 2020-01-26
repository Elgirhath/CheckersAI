class Move:
    def __init__(self, piece, destSquare, killedPiece):
        self.piece = piece
        self.destSquare = destSquare
        self.killedPiece = killedPiece

    def execute(self):
        if self.killedPiece:
            self.killedPiece.kill()
        self.piece.move(self.destSquare)

    def __eq__(self, other):
        return self.piece == other.piece and self.destSquare == other.destSquare and self.killedPiece == other.killedPiece