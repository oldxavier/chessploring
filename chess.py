# This will be the main running script for a chess game.
# First implementation won't have any GUI, that is a
# completely different coding effort that can be done
# after the engine is working sufficiently.

# Initialise chess board, move stack, etc.

# Ask for move input, if empty, "simulate"

# Continue doing so until checkmate or stalemate or draw by not sufficient material or repetition

import create_board
import possible_moves
import play_functions
import sys
sys.setrecursionlimit(10000)

result = 0
no_of_matches = 0

# Function below currently modified for automatic play broken by the return in line 46 for profiling purposes
def play(board):
    # User input
    while True:
        this_move = [] # input("Enter move for {}!".format(board.turn))
        if len(this_move) == 0:
            if board.turn == 1:
                next_move = play_functions.choose_next_move2(board)
            else:
                next_move = play_functions.test_random_move(board)
            if next_move == None:
                global result
                global no_of_matches
                result += board.turn * -1
                no_of_matches += 1
                print("Game over, {} won. Score is: {}/{}".format(board.turn * -1, result, no_of_matches))
                board = create_board.initial_board()
                if no_of_matches == 10:
                    return
                play(board)
            # TODO: maybe we don't need a deep copy!
            if next_move == None:
                return
            new_board = play_functions.make_move(board, next_move[0], next_move[1])
            new_board.turn = new_board.turn * -1
            return  # this line is only for profiling
            play(new_board)
            break
        try:
            move_from = (int(this_move[0]), int(this_move[1]))
            move_to = (int(this_move[2]), int(this_move[3]))
            new_board = play_functions.make_move(board, move_from, move_to)
            if possible_moves.is_check(new_board):
                if possible_moves.possible_moves(board) == None:
                    board.turn = board.turn * -1
                    print("Game over, {} won!".format(board.turn))
                    return
                print("Can't leave king in check, try again!")
                continue
        except:
            print("Invalid input, please try again")
        else:
            new_board.turn = new_board.turn * -1
            play(new_board)



board = create_board.initial_board()
# play(board)

import cProfile, pstats, io
pr = cProfile.Profile()
pr.enable()
play(board)
pr.disable()
s = io.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())