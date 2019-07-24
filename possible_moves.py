# List all possible moves by the player whose turn it is

# Required input: current board, previous board (or last move)

# Don't forget double pawn move, en passant, castling both sides

# Use is_check.py to check whether move is legal

import copy


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
    # Hit En Passant
    if board.en_passant[0] != None:
        if board.en_passant[0][0] == piece[0] and abs(board.en_passant[0][1] - piece[1]) == 1:
            board.en_passant[1] = True
            new_piece = (board.en_passant[0][0] + forward, board.en_passant[0][1])
            if not check_this_move(board, piece, new_piece):
                moves.append((piece, new_piece))
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
    # TODO: Castle
    return moves


def check_this_move(board, move_from, move_to):
    # En passant check
    if board.en_passant[1] == True:
        return check_en_passant_move(board, move_from, move_to)
    # Promotion check
    if (move_to[0] == 8 or move_to[0] == 1) and board.pieces[move_from].type == "Pawn":
        return check_promotion_move(board, move_from, move_to)
    # King move check
    if board.pieces[move_from].type == "King":
        # Castle check
        if abs(move_to[1] - move_from[1]) == 2:
            return check_castle_move(board, move_from, move_to)
        # Normal king move
        else:
            return check_king_move(board, move_from, move_to)
    # Temp variables to reverse move
    temp_type = board.pieces[move_to].type
    temp_colour = board.pieces[move_to].colour
    # Make move
    board.pieces[move_to].type = board.pieces[move_from].type
    board.pieces[move_to].colour = board.pieces[move_from].colour
    board.pieces[move_from].type = None
    board.pieces[move_from].colour = None
    # Is it in check?
    check = is_check(board)
    # Undo move
    board.pieces[move_from].type = board.pieces[move_to].type
    board.pieces[move_from].colour = board.pieces[move_to].colour
    board.pieces[move_to].type = temp_type
    board.pieces[move_to].colour = temp_colour
    return check


def check_king_move(board, move_from, move_to):
    temp_type = board.pieces[move_to].type
    temp_colour = board.pieces[move_to].colour
    # Make move
    board.pieces[move_to].type = "King"
    board.pieces[move_to].colour = board.turn
    board.pieces[move_from].type = None
    board.pieces[move_from].colour = None
    if board.turn == 1:
        board.white_k = move_to
    else:
        board.black_k = move_to
    # Is it in check?
    check = is_check(board)
    # Undo move
    board.pieces[move_to].type = temp_type
    board.pieces[move_to].colour = temp_colour
    board.pieces[move_from].type = "King"
    board.pieces[move_from].colour = board.turn
    if board.turn == 1:
        board.white_k = move_from
    else:
        board.black_k = move_from
    return check


def check_castle_move(board, move_from, move_to):
    if move_to[1] == 7:
        old_rook = (move_from[0], 8)
        new_rook = (move_from[0], 6)
    else:
        old_rook = (move_from[0], 1)
        new_rook = (move_from[0], 4)
    mid_king = (move_from[0], (move_to + move_from) / 2)
    # Initial check
    check1 = is_check(board)
    # Midway check
    board.pieces[mid_king].type = "King"
    board.pieces[mid_king].colour = board.turn
    board.pieces[move_from].type = None
    board.pieces[move_from].colour = None
    if board.turn == 1:
        board.white_k = mid_king
    else:
        board.black_k = mid_king
    check2 = is_check(board)
    # Final check
    board.pieces[move_to].type = "King"
    board.pieces[move_to].colour = board.turn
    board.pieces[mid_king].type = None
    board.pieces[mid_king].colour = None
    if board.turn == 1:
        board.white_k = move_to
    else:
        board.black_k = move_to
    board.pieces[new_rook].type = "Rook"
    board.pieces[new_rook].colour = board.turn
    board.pieces[old_rook].type = None
    board.pieces[old_rook].colour = None
    check3 = is_check(board)
    # Undo move
    board.pieces[move_to].type = None
    board.pieces[move_to].colour = None
    board.pieces[move_from].type = "King"
    board.pieces[move_from].colour = board.turn
    if board.turn == 1:
        board.white_k = move_from
    else:
        board.black_k = move_from
    board.pieces[new_rook].type = None
    board.pieces[new_rook].colour = None
    board.pieces[old_rook].type = "Rook"
    board.pieces[old_rook].colour = board.turn
    return (check1 or check2 or check3)


def check_promotion_move(board, move_from, move_to):
    temp_type = board.pieces[move_to].type
    temp_colour = board.pieces[move_to].colour
    # Make move
    board.pieces[move_to].type = "Queen"
    board.pieces[move_to].colour = board.turn
    board.pieces[move_from].type = None
    board.pieces[move_from].colour = None
    # Is it in check?
    check = is_check(board)
    # Undo move
    board.pieces[move_to].type = temp_type
    board.pieces[move_to].colour = temp_colour
    board.pieces[move_from].type = "Pawn"
    board.pieces[move_from].colour = board.turn
    return check


def check_en_passant_move(board, move_from, move_to):
    board.en_passant[1] = False
    opponent_pawn = (move_to[0] - board.turn, move_to[1])
    # Make move
    board.pieces[move_to].type = "Pawn"
    board.pieces[move_to].colour = board.turn
    board.pieces[move_from].type = None
    board.pieces[move_from].colour = None
    board.pieces[opponent_pawn].type = None
    board.pieces[opponent_pawn].colour = None
    # Is it in check?
    check = is_check(board)
    # Undo move
    board.pieces[move_to].type = None
    board.pieces[move_to].colour = None
    board.pieces[move_from].type = "Pawn"
    board.pieces[move_from].colour = board.turn
    board.pieces[opponent_pawn].type = "Pawn"
    board.pieces[opponent_pawn].colour = board.turn * -1
    return check


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
                if board.pieces[square].type == "Rook" or board.pieces[square].type == "Queen":
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
                if board.pieces[square].type == "Bishop" or board.pieces[square].type == "Queen":
                    return True
                else:
                    break
            elif board.pieces[square].colour == None:
                if direction[0] > 0: direction[0] += 1
                elif direction[0] < 0: direction[0] -= 1
                if direction[1] > 0: direction[1] += 1
                elif direction[1] < 0: direction[1] -= 1
    # Kings
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            square = (king[0] + i, king[1] + j)
            if square in board.pieces and board.pieces[square].colour == board.turn * -1 and board.pieces[square].type == "King":
                return True
    return False
