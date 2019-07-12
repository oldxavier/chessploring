# List all possible moves by the player whose turn it is

# Required input: current board, previous board (or last move)

# Don't forget double pawn move, en passant, castling both sides

# Use is_check.py to check whether move is legal

import copy


def flip_to_move(to_move):
    if to_move == "W":
        return "B"
    else:
        return "W"

def check_this_move(board, move_from, move_to):
    # Promotion check
    if (move_to[0] == 8 or move_to[0] == 1) and board.pieces[move_from].type == "Pawn":
        promotion = True
    else:
        promotion = False
    # Whose turn it is
    to_move = board.pieces[move_from].colour
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
    # Check or not
    check = is_check(board, to_move)
    # Reverse move
    if promotion:
        board.pieces[move_from].type = "Pawn"
    else:
        board.pieces[move_from].type = board.pieces[move_to].type
    board.pieces[move_from].colour = board.pieces[move_to].colour
    board.pieces[move_to].type = temp_type
    board.pieces[move_to].colour = temp_colour
    # Return boolean
    return check


def possible_moves(board, to_move):
    moves = []
    for piece in board.pieces:
        if board.pieces[piece].colour != to_move:
            continue
        if board.pieces[piece].type == "Pawn":
            moves.extend(possible_pawn_moves(board, piece, to_move))
        elif board.pieces[piece].type == "Rook":
            moves.extend(possible_rook_moves(board, piece, to_move))
        # elif board.pieces[piece].type == "Knight":
        #     #moves.extend(possible_knight_moves(board, piece, to_move))
        # elif board.pieces[piece].type == "Bishop":
        #     #moves.extend(possible_bishop_moves(board, piece, to_move))
        # elif board.pieces[piece].type == "Queen":
        #     #moves.extend(possible_queen_moves(board, piece, to_move))
        # elif board.pieces[piece].type == "King":
        #     #moves.extend(possible_king_moves(board, piece, to_move))
    if len(moves) == 0:
        return None
    else:
        return moves
    
def possible_pawn_moves(board, piece, to_move):
    moves = []
    if to_move == "W":
        forward = 1
    else:
        forward = -1
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
        if board.pieces[new_piece].colour != to_move and board.pieces[new_piece].colour != None:
            if not check_this_move(board, piece, new_piece):
                moves.append((piece, new_piece))
    # Hit Right (white's perspective)
    if piece[1] < 8:
        new_piece = (piece[0] + forward, piece[1] + 1)
        if board.pieces[new_piece].colour != to_move and board.pieces[new_piece].colour != None:
            if not check_this_move(board, piece, new_piece):
                moves.append((piece, new_piece))
    # TODO: Hit En Passant
    return moves

def possible_rook_moves(board, piece, to_move):
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
                elif board.pieces[new_piece].colour != to_move:
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

def is_check(board, to_move):
    # TODO: track/query king's position
    # TODO: king cannot move next to other king
    if to_move == "W":
        forward = 1
        king = (1,5)
    else:
        forward = -1
        king = (8,5)
    # Pawns
    p1 = (king[0] + forward, king[1] + 1)
    p2 = (king[0] + forward, king[1] - 1)
    if p1 in board.pieces and board.pieces[p1].type == "Pawn" and board.pieces[p1].colour == flip_to_move(to_move):
        return True
    if p2 in board.pieces and board.pieces[p2].type == "Pawn" and board.pieces[p2].colour == flip_to_move(to_move):
        return True
    # Knights
    knights = [ (king[0]-2, king[1]-1), (king[0]-2, king[1]+1), (king[0]-1, king[1]-2), (king[0]-1, king[1]+2), (king[0]+1, king[1]-2), (king[0]+1, king[1]+2), (king[0]+2, king[1]-1), (king[0]+2, king[1]+1) ]
    for knight in knights:
        if knight in board.pieces and board.pieces[knight].type == "Knight" and board.pieces[knight].colour == flip_to_move(to_move):
            return True
    # Rooks (and Queens)
    directions = [ [1,0], [0,1], [-1,0], [0,-1] ]
    for direction in directions:
        while True:
            square = (king[0] + direction[0], king[1] + direction[1])
            if square not in board.pieces or board.pieces[square].colour == to_move:
                break
            if board.pieces[square].colour == flip_to_move(to_move):
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
            if square not in board.pieces or board.pieces[square].colour == to_move:
                break
            if board.pieces[square].colour == flip_to_move(to_move):
                if board.pieces[square].type == "Bishop" or board.pieces[square].type == "Queen":
                    return True
                else:
                    break
            elif board.pieces[square].colour == None:
                if direction[0] > 0: direction[0] += 1
                elif direction[0] < 0: direction[0] -= 1
                if direction[1] > 0: direction[1] += 1
                elif direction[1] < 0: direction[1] -= 1
    return False


# Old check function, slow, won't use
def is_check2(board, to_move):
    check = False
    if to_move == "W":
        forward = 1
    else:
        forward = -1
    other = flip_to_move(to_move)
    pawns = []
    rooks = []
    knights = []
    bishops = []
    queens = []
    for square in board.pieces:
        if board.pieces[square].type == "King" and board.pieces[square].colour == to_move:
            king = square
        if board.pieces[square].colour == other:
            if board.pieces[square].type == "Pawn":
                pawns.append(square)
            elif board.pieces[square].type == "Rook":
                rooks.append(square)
            elif board.pieces[square].type == "Knight":
                knights.append(square)
            elif board.pieces[square].type == "Bishop":
                bishops.append(square)
            elif board.pieces[square].type == "Queen":
                queens.append(square)

    for pawn in pawns:
        if king[0] + forward == pawn[0] and (king[1] - 1 == pawn[1] or king[1] + 1 == pawn[1]):
            return True

    for rook in rooks:
        # Same row
        if king[0] == rook[0]:
            diff = abs(king[1] - rook[1])
            smaller = min(king[1], rook[1])
            # For each square in between, check if occupied. If none are, return True.
            rook_check = True
            for i in range(1, diff):
                if board.pieces[(king[0], smaller + i)].type != None:
                    rook_check = False
                    break
            if rook_check:
                return True
        # Same column
        if king[1] == rook[1]:
            diff = abs(king[0] - rook[0])
            smaller = min(king[0], rook[0])
            # For each square in between, check if occupied. If none are, return True.
            rook_check = True
            for i in range(1, diff):
                if board.pieces[(smaller + i, king[1])].type != None:
                    rook_check = False
                    break
            if rook_check:
                return True

    for knight in knights:
        if abs((king[0] - knight[0]) * (king[1] - knight[1])) == 2:
            return True

    for bishop in bishops:
        if abs(king[0] - bishop[0]) == abs(king[1] - bishop[1]):
            check = True
            diff = king[0] - bishop[0]
            if diff == 1:
                return True
            if king[0] < bishop[0]:
                r = 1
            else:
                r = -1
            if king[1] < bishop[1]:
                c = 1
            else:
                c = -1
            for i in range(1, diff):
                if board.pieces[(king[0] + r*i, king[1] + c*i)].type != None:
                    check = False
                    break
            if check == True:
                return True
    
    for queen in queens:
        # Rook part
        if king[0] == queen[0]:
            check = True
            diff = abs(king[1] - queen[1])
            if diff == 1:
                return True
            smaller = min(king[1], queen[1])
            for i in range(1, diff):
                if board.pieces[(king[0], smaller + i)].type != None:
                    check = False
                    break
            if check == True:
                return True
        if king[1] == queen[1]:
            check = True
            diff = abs(king[0] - queen[0])
            if diff == 1:
                return True
            smaller = min(king[0], queen[0])
            for i in range(1, diff):
                if board.pieces[(smaller + i, king[1])].type != None:
                    check = False
                    break
            if check == True:
                return True
        # Bishop part
        if abs(king[0] - queen[0]) == abs(king[1] - queen[1]):
            check = True
            diff = king[0] - queen[0]
            if diff == 1:
                return True
            if king[0] < queen[0]:
                r = 1
            else:
                r = -1
            if king[1] < queen[1]:
                c = 1
            else:
                c = -1
            for i in range(1, diff):
                if board.pieces[(king[0] + r*i, king[1] + c*i)].type != None:
                    check = False
                    break
            if check == True:
                return True
    return False
