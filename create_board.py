class Piece:
    def __init__(self, this_type, this_colour):
        self.type = this_type
        self.colour = this_colour

class Board():
    def __init__(self, pieces, castle):
        self.pieces = pieces
        self.castle = castle

def initial_board():
    # TODO: populate initial board with 64 pieces
    initial_board = None
    return initial_board