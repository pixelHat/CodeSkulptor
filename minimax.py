"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(20)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.

    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    win = board.check_win()
    if win != None:
        return SCORES[win], (-1, -1)
    else:
        lst = []
        possibles_moves = board.get_empty_squares()
        for moves in possibles_moves:
            new_board = board.clone()
            new_board.move(moves[0], moves[1], player)
            new_player = provided.switch_player(player)
            move = mm_move(new_board, new_player)
            if player == provided.PLAYERO:
                if move[0] == -1:
                    return move[0], moves
            else:
                if move[0] == 1:
                    return move[0], moves
            lst.append((move[0], moves))

        if player == provided.PLAYERO:
            return min(lst)
        else:
            return max(lst)


def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)
poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
