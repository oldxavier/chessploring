import random
import possible_moves
import copy
import sys


def make_move(board, move_from, move_to):
    new_board = copy.deepcopy(board)
    # Promotion
    if (move_to[0] == 8 or move_to[0] == 1) and new_board.pieces[move_from].type == "Pawn":
        new_board.pieces[move_from].type = "Queen"
    # King move
    if new_board.pieces[move_from].type == "King":
        if new_board.turn == 1:
            new_board.white_k = move_to
        else:
            new_board.black_k = move_to
    # En Passant enabler move
    if abs(move_from[0] - move_to[0]) == 2 and new_board.pieces[move_from] == "Pawn":
        new_board.en_passant[0] = move_to
    else:
        new_board.en_passant[0] = None
    # En Passant move
    if move_from[1] != move_to[1] and new_board.pieces[move_from].type == "Pawn" and new_board.pieces[move_to].type == None:
        new_board.pieces[(move_to[0], move_from[1])].type = None
        new_board.pieces[(move_to[0], move_from[1])].colour = None
    # Move
    new_board.pieces[move_to].type = new_board.pieces[move_from].type
    new_board.pieces[move_to].colour = new_board.pieces[move_from].colour
    new_board.pieces[move_from].type = None
    new_board.pieces[move_from].colour = None
    return new_board

def choose_next_move(board, no_of_searches):
    no_of_wins = 0
    moves = possible_moves.possible_moves(board)
    best_move = None
    if moves == None:
        return None
    to_win = board.turn
    random.shuffle(moves)
    for move in moves:
        this_board = make_move(board, move[0], move[1])
        mc_board = copy.deepcopy(this_board)
        this_no_of_wins = 0
        for i in range(no_of_searches):
            mc_board.white_k = this_board.white_k
            mc_board.black_k = this_board.black_k
            mc_board.en_passant = this_board.en_passant
            for piece in this_board.pieces:
                mc_board.pieces[piece].type = this_board.pieces[piece].type
                mc_board.pieces[piece].colour = this_board.pieces[piece].colour
            this_no_of_wins += recursive_mc_search(mc_board, to_win)
        if this_no_of_wins > no_of_wins:
            no_of_wins = this_no_of_wins
            best_move = move
    print(best_move)
    return best_move

def choose_next_move2(board):
    moves = possible_moves.possible_moves(board)
    if moves == None:
        return None
    max_min_result = -sys.maxsize
    to_win = board.turn
    random.shuffle(moves)
    for move in moves:
        board_opponent = make_move(board, move[0], move[1])
        board_opponent.turn = board_opponent.turn * -1
        moves_opponent = possible_moves.possible_moves(board_opponent)
        if moves_opponent == None:
            return None
        min_result = sys.maxsize
        random.shuffle(moves_opponent)
        for move_opponent in moves_opponent:
            board_us = make_move(board_opponent, move_opponent[0], move_opponent[1])
            board_us.turn = board_us.turn * -1
            moves_us = possible_moves.possible_moves(board_us)
            if moves_us == None:
                return None
            result = 0
            random.shuffle(moves_us)
            for move_us in moves_us:
                board_opponent_2 = make_move(board_us, move_us[0], move_us[1])
                result += recursive_mc_search(board_opponent_2, to_win)
            result = result / len(moves_us)
            if result < min_result:
                min_result = result
        if min_result > max_min_result:
            max_min_result = min_result
            best_move = move
    return best_move
    
        
            



def recursive_mc_search(mc_board, to_win):
    # Flip turn
    mc_board.turn = mc_board.turn * -1
    mc_moves = possible_moves.possible_moves(mc_board)
    if mc_moves == None:
        if mc_board.turn == to_win:
            if possible_moves.is_check(mc_board) == True: return -1
            else: return 0
        else:
            if possible_moves.is_check(mc_board) == True: return 1
            else: return 0
    random.shuffle(mc_moves)
    new_move = mc_moves[0]
    if abs(new_move[0][0] - new_move[1][0]) == 2 and mc_board.pieces[new_move[0]].type == "Pawn":
        # Enable en passant
        mc_board.en_passant[0] = new_move[1]
    else:
        mc_board.en_passant[0] = None
    if new_move[0][1] != new_move[1][1] and mc_board.pieces[new_move[0]].type == "Pawn" and mc_board.pieces[new_move[1]].type == None:
        # En passant move
        mc_board.pieces[(new_move[1][0], new_move[0][1])].type = None
        mc_board.pieces[(new_move[1][0], new_move[0][1])].colour = None
    if (new_move[1][0] == 8 or new_move[1][0] == 1) and mc_board.pieces[new_move[0]].type == "Pawn":
        # Promotion
        mc_board.pieces[new_move[1]].type = "Queen"
    else:
        mc_board.pieces[new_move[1]].type = mc_board.pieces[new_move[0]].type
    mc_board.pieces[new_move[1]].colour = mc_board.pieces[new_move[0]].colour
    mc_board.pieces[new_move[0]].type = None
    mc_board.pieces[new_move[0]].colour = None
    if mc_board.pieces[new_move[1]].type == "King":
        if mc_board.turn == 1:
            mc_board.white_k = new_move[1]
        else:
            mc_board.black_k = new_move[1]
    return recursive_mc_search(mc_board, to_win)

def test_random_move(board):
    moves = possible_moves.possible_moves(board)
    if moves == None:
        return None
    random.shuffle(moves)
    print(moves[0])
    return moves[0]