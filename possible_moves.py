# List all possible moves by the player whose turn it is

# Required input: current board, previous board (or last move)

# Don't forget double pawn move, en passant, castling both sides

# Use is_check.py to check whether move is legal

import copy


def check_this_move(board, move_from, move_to):
    # Promotion check
    if (move_to[0] == 8 or move_to[0] == 1) and board.pieces[move_from].type == "Pawn":
        promotion = True
    else:
        promotion = False
    # King move check
    if board.pieces[move_from].type == "King":
        kingmove = True
    else:
        kingmove = False
    # Temp variables to reverse move
    temp_type = board.pieces[move_to].type
    temp_colour = board.pieces[move_to].colour
    # Make move
    if promotion:
        board.pieces[move_to].type = "Queen"
    else:
        board.pieces[move_to].type = board.pieces[move_from].type
    board.pieces[move_to].colour = board.pieces[move_from].colour
    board.pieces[move_from].type = None
    board.pieces[move_from].colour = None
    if kingmove:
        if board.turn == 1:
            board.white_k = move_to
        else:
            board.black_k = move_to
    # Check or not
    check = is_check(board)
    # Reverse move
    if promotion:
        board.pieces[move_from].type = "Pawn"
    else:
        board.pieces[move_from].type = board.pieces[move_to].type
    board.pieces[move_from].colour = board.pieces[move_to].colour
    board.pieces[move_to].type = temp_type
    board.pieces[move_to].colour = temp_colour
    if kingmove:
        if board.turn == 1:
            board.white_k = move_from
        else:
            board.black_k = move_from
    # Return boolean
    return check


def possible_moves(board):
    count = 0
    moves = []
    for piece in board.pieces:
        if board.pieces[piece].type != None:
            count += 1
        if board.pieces[piece].colour != board.turn:
            continue
        if board.pieces[piece].type == "Pawn":
            moves.extend(possible_pawn_moves(board, piece))
        elif board.pieces[piece].type == "Rook":
            moves.extend(possible_rook_moves(board, piece))
        elif board.pieces[piece].type == "Knight":
            moves.extend(possible_knight_moves(board, piece))
        elif board.pieces[piece].type == "Bishop":
            moves.extend(possible_bishop_moves(board, piece))
        elif board.pieces[piece].type == "Queen":
            moves.extend(possible_rook_moves(board, piece))
            moves.extend(possible_bishop_moves(board, piece))
        elif board.pieces[piece].type == "King":
            moves.extend(possible_king_moves(board, piece))
    if len(moves) == 0 or count < 5:
        return None
    else:
        return moves
    
def possible_pawn_moves(board, piece):
    moves = []
    forward = board.turn
    # One forward
    new_piece = (piece[0] + forward, piece[1])
    if new_piece in board.pieces and board.pieces[new_piece].type == None:
        if not check_this_move(board, piece, new_piece):
            moves.append((piece, new_piece))
    # Two forward
    middle_piece = (piece[0] + forward, piece[1])
    new_piece = (piece[0] + 2*forward, piece[1])
    if piece[0] == 4.5 - 2.5*forward and board.pieces[middle_piece].type == None and board.pieces[new_piece].type == None:
        if not check_this_move(board, piece, new_piece):
            moves.append((piece, new_piece))
    # Hit Left (white's perspective)
    if piece[1] > 1:
        new_piece = (piece[0] + forward, piece[1] - 1)
        if board.pieces[new_piece].colour != board.turn and board.pieces[new_piece].colour != None:
            if not check_this_move(board, piece, new_piece):
                moves.append((piece, new_piece))
    # Hit Right (white's perspective)
    if piece[1] < 8:
        new_piece = (piece[0] + forward, piece[1] + 1)
        if board.pieces[new_piece].colour != board.turn and board.pieces[new_piece].colour != None:
            if not check_this_move(board, piece, new_piece):
                moves.append((piece, new_piece))
    # TODO: Hit En Passant
    return moves

def possible_rook_moves(board, piece):
    moves = []
    directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    for direction in directions:
        while True:
            new_piece = (piece[0] + direction[0], piece[1] + direction[1])
            # Check that square is within board
            if new_piece in board.pieces:
                # Check that square is empty
                if board.pieces[new_piece].colour == None:
                    # Check that we aren't in check after the move
                    if not check_this_move(board, piece, new_piece):
                        moves.append((piece, new_piece))
                # Check that we are hitting the opponent
                elif board.pieces[new_piece].colour != board.turn:
                    # Check that we aren't in check after the move
                    if not check_this_move(board, piece, new_piece):
                        moves.append((piece, new_piece))
                    # We encountered a piece so we can't move any further in this direction, break
                    break
                # We would be hitting our own piece, so we break
                else:
                    break
                # Move one square further in the current direction
                if direction[0] > 0:
                    direction[0] += 1
                elif direction[0] < 0:
                    direction[0] -= 1
                if direction[1] > 0:
                    direction[1] += 1
                elif direction[1] < 0:
                    direction[1] -= 1
            # We got out of bounds, so we break
            else:
                break
    return moves

def possible_knight_moves(board, piece):
    moves = []
    squares = [ (piece[0]-2, piece[1]-1), (piece[0]-2, piece[1]+1), 
                (piece[0]-1, piece[1]-2), (piece[0]-1, piece[1]+2), 
                (piece[0]+1, piece[1]-2), (piece[0]+1, piece[1]+2), 
                (piece[0]+2, piece[1]-1), (piece[0]+2, piece[1]+1) ]
    for square in squares:
        if square in board.pieces and board.pieces[square].colour != board.turn and not check_this_move(board, piece, square):
            moves.append((piece, square))
    return moves

def possible_bishop_moves(board, piece):
    moves = []
    directions = [ [1,1], [1,-1], [-1,1], [-1,-1] ]
    for direction in directions:
        while True:
            square = (piece[0] + direction[0], piece[1] + direction[1])
            if square not in board.pieces or board.pieces[square].colour == board.turn:
                break
            if not check_this_move(board, piece, square):
                moves.append((piece, square))
            if board.pieces[square].colour == board.turn * -1:
                break
            if direction[0] > 0: direction[0] += 1
            elif direction[0] < 0: direction[0] -= 1
            if direction[1] > 0: direction[1] += 1
            elif direction[1] < 0: direction[1] -= 1
    return moves

def possible_king_moves(board, piece):
    moves = []
    directions = [ [1,1], [1,0], [1,-1], [0,1], [0,-1], [-1,1], [-1,0], [-1,-1] ]
    for direction in directions:
        square = (piece[0] + direction[0], piece[1] + direction[1])
        if square in board.pieces and board.pieces[square].colour != board.turn and not check_this_move(board, piece, square):
            moves.append((piece, square))
    return moves

def is_check(board):
    forward = board.turn
    if board.turn == 1:
        king = board.white_k
    else:
        king = board.black_k
    # Pawns
    p1 = (king[0] + forward, king[1] + 1)
    p2 = (king[0] + forward, king[1] - 1)
    if p1 in board.pieces and board.pieces[p1].type == "Pawn" and board.pieces[p1].colour == board.turn * -1:
        return True
    if p2 in board.pieces and board.pieces[p2].type == "Pawn" and board.pieces[p2].colour == board.turn * -1:
        return True
    # Knights
    for i in range(-1, 2, 2):
        for j in range(-2, 5, 4):
            square1 = (king[0] + i, king[1] + j)
            if square1 in board.pieces and board.pieces[square1].type == "Knight" and board.pieces[square1].colour == board.turn * -1:
                return True
            square2 = (king[0] + j, king[1] + i)
            if square2 in board.pieces and board.pieces[square2].type == "Knight" and board.pieces[square2].colour == board.turn * -1:
                return True
    # Rooks (and Queens)
    directions = [ [1,0], [0,1], [-1,0], [0,-1] ]
    for direction in directions:
        while True:
            square = (king[0] + direction[0], king[1] + direction[1])
            if square not in board.pieces or board.pieces[square].colour == board.turn:
                break
            if board.pieces[square].colour == board.turn * -1:
                if board.pieces[square].type == "Rook" or board.pieces[square].type == "Queen" or board.pieces[square].type == "King":
                    return True
                else:
                    break
            elif board.pieces[square].colour == None:
                if direction[0] > 0: direction[0] += 1
                elif direction[0] < 0: direction[0] -= 1
                if direction[1] > 0: direction[1] += 1
                elif direction[1] < 0: direction[1] -= 1
    # Bishops (and Queens)
    directions = [ [1,1], [1,-1], [-1,1], [-1,-1] ]
    for direction in directions:
        while True:
            square = (king[0] + direction[0], king[1] + direction[1])
            if square not in board.pieces or board.pieces[square].colour == board.turn:
                break
            if board.pieces[square].colour == board.turn * -1:
                if board.pieces[square].type == "Bishop" or board.pieces[square].type == "Queen" or board.pieces[square].type == "King":
                    return True
                else:
                    break
            elif board.pieces[square].colour == None:
                if direction[0] > 0: direction[0] += 1
                elif direction[0] < 0: direction[0] -= 1
                if direction[1] > 0: direction[1] += 1
                elif direction[1] < 0: direction[1] -= 1
    return False
