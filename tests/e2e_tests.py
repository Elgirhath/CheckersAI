from pawn import Pawn
from queen import Queen

def setup(boardBuilder):
    white = [
        (Pawn, 1, 1),
        (Queen, 5, 3)
    ]
    black = [
        (Pawn, 6, 6),
        (Queen, 0, 6)
    ]
    boardBuilder.build(boardBuilder.convertToSettings(white, black))

def trap_a_queen(boardBuilder):
    white = [
        (Pawn, 5, 0),
        (Pawn, 4, 5),
        (Pawn, 7, 6),
        (Queen, 6, 5)
    ]
    black = [
        (Pawn, 0, 1),
        (Pawn, 1, 0),
        (Pawn, 2, 3),
        (Pawn, 2, 5),
        (Pawn, 1, 6)
    ]
    boardBuilder.build(boardBuilder.convertToSettings(white, black))
    
def if_promotion_is_best_then_promote(boardBuilder):
    white = [
        (Pawn, 5, 0),
        (Pawn, 4, 5),
        (Pawn, 7, 6),
    ]
    black = [
        (Pawn, 0, 1),
        (Pawn, 1, 0),
        (Pawn, 2, 3),
        (Pawn, 2, 5),
        (Pawn, 6, 3)
    ]
    boardBuilder.build(boardBuilder.convertToSettings(white, black))

def win_the_game_if_possible(boardBuilder):
    white = [
        (Pawn, 5, 0),
        (Pawn, 4, 5),
        (Pawn, 7, 6),
    ]
    black = [
        (Pawn, 0, 1),
        (Pawn, 1, 0),
        (Pawn, 2, 3),
        (Pawn, 2, 5),
        (Pawn, 6, 3)
    ]
    boardBuilder.build(boardBuilder.convertToSettings(white, black))