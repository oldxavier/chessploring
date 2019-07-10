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
    pieces = {}
    for i in range(1,9):
        for j in range(1,9):
            pieces[(i,j)] = Piece(None, None)
    # Colours
    for piece in pieces:
        if piece[0] > 2 and piece[0] < 7:
            continue
        elif piece[0] < 3:
            pieces[piece].colour = "W"
        else:
            pieces[piece].colour = "B"
    # Types
    for piece in pieces:
        if piece[0] > 2 and piece[0] < 7:
            continue
        elif piece[0] == 2 or piece[0] == 7:
            pieces[piece].type = "Pawn"
        elif piece[1] == 1 or piece[1] == 8:
            pieces[piece].type = "Rook"
        elif piece[1] == 2 or piece[1] == 7:
            pieces[piece].type = "Knight"
        elif piece[1] == 3 or piece[1] == 6:
            pieces[piece].type = "Bishop"
        elif piece[1] == 4:
            pieces[piece].type = "Queen"
        elif piece[1] == 5:
            pieces[piece].type = "King"
    # Create board
    castle = [True, True, True, True]
    initial_board = Board(pieces, castle)
    return initial_board

initial_board()