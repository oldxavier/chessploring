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


def play(board, to_move):
    # User input
    while True:
        this_move = [] # input("Enter move for {}!".format(to_move))
        if len(this_move) == 0:
            next_move = play_functions.choose_next_move(board, to_move)
            to_move = play_functions.flip_to_move(to_move)
            if next_move == None:
                print("Game over, {} won!".format(to_move))
                return
            # TODO: maybe we don't need a deep copy!
            new_board = play_functions.make_move(board, next_move[0], next_move[1])
            # return  # this line is only for profiling
            play(new_board, to_move)
            break
        try:
            move_from = (this_move[0], this_move[1])
            move_to = (this_move[2], this_move[3])
            new_board = play_functions.move(board, move_from, move_to)
            if possible_moves.is_check(new_board, to_move):
                if possible_moves.possible_moves(board, to_move) == None:
                    to_move = play_functions.flip_to_move(to_move)
                    print("Game over, {} won!".format(to_move))
                    break
                print("Can't leave king in check, try again!")
                continue
        except:
            "Invalid input, please try again"
        else:
            to_move = play_functions.flip_to_move(to_move)
            play(new_board, to_move)


board = create_board.initial_board()
to_move = "W"
play(board, to_move)



# import cProfile, pstats, io
# pr = cProfile.Profile()
# pr.enable()
# play(board, to_move)
# pr.disable()
# s = io.StringIO()
# sortby = 'cumulative'
# ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
# ps.print_stats()
# print(s.getvalue())