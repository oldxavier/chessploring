# List all possible moves by the player whose turn it is

# Required input: current board, previous board (or last move)

# Don't forget double pawn move, en passant, castling both sides

# Use is_check.py to check whether move is legal

def flip_to_move(to_move):
    if to_move == "W":
        return "B"
    else:
        return "W"

def move(board, move_from, move_to):
    board[move_to] = board[move_from]
    board[move_from].type = None
    board[move_from].colour = None
    return board

def possible_moves(board, to_move):
    moves = []
    for piece in board:
        if board[piece].type == None:
            continue
        if board[piece].type == "Pawn":
            moves.extend(possible_pawn_moves(board, piece, to_move))
        elif board[piece].type == "Rook":
            moves.extend(possible_rook_moves(board, piece, to_move))
        # elif board[piece].type == "Knight":
        #     #moves.extend(possible_knight_moves(board, piece, to_move))
        # elif board[piece].type == "Bishop":
        #     #moves.extend(possible_bishop_moves(board, piece, to_move))
        # elif board[piece].type == "Queen":
        #     #moves.extend(possible_queen_moves(board, piece, to_move))
        # elif board[piece].type == "King":
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
    if board[new_piece].type == None:
        new_board = move(board, piece, new_piece)
        if new_piece[0] == 4.5 + 3.5*forward:
            new_board[new_piece].type = "Queen"
        if not is_check(new_board, to_move):
            moves.append(new_board)
    # Two forward
    middle_piece = (piece[0] + forward, piece[1])
    new_piece = (piece[0] + 2*forward, piece[1])
    if piece[0] == 4.5 - 2.5*forward and board[middle_piece].type == None and board[new_piece].type == None:
        new_board = move(board, piece, new_piece)
        if not is_check(new_board, to_move):
            moves.append(new_board)
    # Hit Left (white's perspective)
    if piece[1] > 1:
        new_piece = board[(piece[0] + forward, piece[1] - 1)]
        if new_piece.colour != to_move and new_piece.colour != None:
            new_board = move(board, piece, new_piece)
            if new_piece[0] == 4.5 + 3.5*forward:
                new_board[new_piece].type = "Queen"
            if not is_check(new_board, to_move):
                moves.append(new_board)
    # Hit Right (white's perspective)
    if piece[1] < 8:
        new_piece = board[(piece[0] + forward, piece[1] + 1)]
        if new_piece.colour != to_move and new_piece.colour != None:
            new_board = move(board, piece, new_piece)
            if new_piece[0] == 4.5 + 3.5*forward:
                new_board[new_piece].type = "Queen"
            if not is_check(new_board, to_move):
                moves.append(new_board)
    # TODO: Hit En Passant
    return moves

def possible_rook_moves(board, piece, to_move):
    moves = []
    return moves

def is_check(board, to_move):
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
        if king[0] == rook[0]:
            check = True
            diff = abs(king[1], rook[1])
            if diff == 1:
                return True
            smaller = min(king[1], rook[1])
            for i in range(1, diff):
                if board.pieces[(king[0], smaller + i)].type != None:
                    check = False
                    break
            if check == True:
                return True
        if king[1] == rook[1]:
            check = True
            diff = abs(king[0], rook[0])
            if diff == 1:
                return True
            smaller = min(king[0], rook[0])
            for i in range(1, diff):
                if board.pieces[(smaller + i, king[1])].type != None:
                    check = False
                    break
            if check == True:
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
            diff = abs(king[1], queen[1])
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
            diff = abs(king[0], queen[0])
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



import create_board

board = create_board.initial_board()
print(is_check(board, "W"))