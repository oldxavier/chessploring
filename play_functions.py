import random
import possible_moves


def flip_to_move(to_move):
    if to_move == "W":
        return "B"
    else:
        return "W"

def move(board, move):
    move_from = (move[0], move[1])
    move_to = (move[2], move[3])
    board[move_to] = board[move_from]
    board[move_from].type = None
    board[move_from].colour = None
    return board

def choose_next_move(board, to_move):
    no_of_searches = 2
    no_of_wins = 0
    moves = possible_moves.possible_moves(board, to_move)
    best_move = None
    if moves == None:
        return None
    to_win = to_move
    to_move = flip_to_move(to_move)
    for move in moves:
        this_no_of_wins = 0
        for i in range(no_of_searches):
            this_no_of_wins += recursive_mc_search(move, to_move, to_win)
        if this_no_of_wins > no_of_wins:
            no_of_wins = this_no_of_wins
            best_move = move
    return best_move

def recursive_mc_search(move, to_move, to_win):
    moves = possible_moves.possible_moves(move, to_move)
    if moves == None:
        # Assumes that stalemate and other draws aren't good enough
        if to_move == to_win:
            return 0
        else:
            return 1
    new_move = random.shuffle(moves)[0]
    to_move = flip_to_move(to_move)
    return recursive_mc_search(new_move, to_move, to_win)