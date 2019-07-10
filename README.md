# chessploring
A self-study attempt to beat myself in chess.
Initial plan: Build a Monte-Carlo search iterating through all possible moves, randomly selecting moves until Game Over N times, then recommending move based on how many of N resulted in a win. For this, we need a fast listing of all possible moves and a fast is_check method. If the list is empty and there is check, that's checkmate. If the list is empty and there is no check, it's stalemate. Must stop search when material isn't sufficient for mate.
