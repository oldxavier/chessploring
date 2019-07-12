import random

class Square:
    def __init__(self, name):
        self.name = name


test = [1, 0, 1, 0, 1, 0, 1, 1, 1]


def possible_moves(a):
    moves = []
    if all(a):
        return moves
    if not any(a):
        return moves
    for index in range(len(a)):
        b = a.copy()
        if a[index]:
            b[index] = 0
        else:
            b[index] = 1
        moves.append(b)
    return moves


def evaluate(board, first_round, max_score):
    moves = possible_moves(board)
    random.shuffle(moves)
    if len(moves) == 0:
        max_score += board[0]
        return board[0]
    if first_round:
        best_move = []
        for move in moves:
            score = evaluate(move, False, max_score)
            if score > max_score:
                max_score = score
                best_move = move
        return best_move
    else:
        return evaluate(moves[0], False, max_score)


print(evaluate(test, True, -100))