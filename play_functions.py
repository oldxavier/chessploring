import random
import possible_moves
import copy


def flip_to_move(to_move):
    if to_move == "W":
        return "B"
    else:
        return "W"

def make_move(board, move_from, move_to):
    new_board = copy.deepcopy(board)
    # Promotion
    if (move_to[0] == 8 or move_to[0] == 1) and new_board.pieces[move_from].type == "Pawn":
        new_board.pieces[move_from].type = "Queen"
    new_board.pieces[move_to].type = new_board.pieces[move_from].type
    new_board.pieces[move_to].colour = new_board.pieces[move_from].colour
    new_board.pieces[move_from].type = None
    new_board.pieces[move_from].colour = None
    return new_board

def choose_next_move(board, to_move):
    no_of_searches = 4
    no_of_wins = 0
    moves = possible_moves.possible_moves(board, to_move)
    best_move = None
    if moves == None:
        return None
    to_win = to_move
    first_to_move = flip_to_move(to_move)
    for move in moves:
        this_board = make_move(board, move[0], move[1])
        mc_board = copy.deepcopy(this_board)
        this_no_of_wins = 0
        for i in range(no_of_searches):
            for piece in this_board.pieces:
                mc_board.pieces[piece].type = this_board.pieces[piece].type
                mc_board.pieces[piece].colour = this_board.pieces[piece].colour
            this_no_of_wins += recursive_mc_search(mc_board, first_to_move, to_win)
        if this_no_of_wins > no_of_wins:
            no_of_wins = this_no_of_wins
            best_move = move
    print(best_move)
    return best_move

def recursive_mc_search(mc_board, to_move, to_win):
    mc_moves = possible_moves.possible_moves(mc_board, to_move)
    if mc_moves == None:
        # Assumes that stalemate and other draws aren't good enough
        if to_move == to_win:
            if possible_moves.is_check(mc_board, to_move) == True:
                return 0
            else:
                return 0.5
        else:
            if possible_moves.is_check(mc_board, to_move) == True:
                return 1
            else:
                return 0.5
    random.shuffle(mc_moves)
    new_move = mc_moves[0]
    if (new_move[1][0] == 8 or new_move[1][0] == 1) and mc_board.pieces[new_move[0]].type == "Pawn":
        mc_board.pieces[new_move[1]].type = "Queen"
    else:
        mc_board.pieces[new_move[1]].type = mc_board.pieces[new_move[0]].type
    mc_board.pieces[new_move[1]].colour = mc_board.pieces[new_move[0]].colour
    mc_board.pieces[new_move[0]].type = None
    mc_board.pieces[new_move[0]].colour = None
    to_move = flip_to_move(to_move)
    return recursive_mc_search(mc_board, to_move, to_win)