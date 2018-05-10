"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 1000        # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player

# Add your functions here.
def mc_trial(board, player):
    """
    This function takes a current board and the next player to move.
    The function should play a game starting with the given player
    by making random moves, alternating between players.
    """
    _board = board
    choose = list(_board.get_empty_squares())
    _player = player

    while _board.check_win() == None:
        play = random.choice(choose)
        _board.move(play[0], play[1], _player)
        _player = provided.switch_player(_player)
        choose = list(_board.get_empty_squares())

def mc_update_scores(scores, board, player = provided.PLAYERX):
    """
    This function takes a grid of scores, a board from a completed game,
    and which player the machine player is. The function should score the
    completed board and update the scores grid.
    """
    scorex, scoreo = 0, 0
    if board.check_win() == provided.PLAYERX:
        scorex = SCORE_CURRENT
        scoreo = - SCORE_OTHER
    elif board.check_win() == provided.PLAYERO:
        scorex = - SCORE_CURRENT
        scoreo = SCORE_OTHER
        
    for row in range(board.get_dim()):
        for field in range(board.get_dim()):
            if board.square(row, field) == provided.PLAYERX:
                scores[row][field] = scorex
            elif board.square(row, field) == provided.PLAYERO:
                scores[row][field] = scoreo

def get_best_move(board, scores):
    """
    This function takes the current board, a grid of scores and return
    the best play.
    """
    maximum = -NTRIALS
    free = board.get_empty_squares()
    choose = []
    for value in free:
        if scores[value[0]][value[1]] > maximum:
            maximum = scores[value[0]][value[1]]

    for value in free:
        if scores[value[0]][value[1]] == maximum:
            choose.append(value)

    return random.choice(choose)

def mc_move(board, player, trials):
    """
    escrever mais tarde
    """
    if board.get_empty_squares() != []:
        scores = [[0 for dummy_i in range(board.get_dim())] for dummy_j in range(board.get_dim())]
        for _ in range(trials):
            _board = board.clone()
            mc_trial(_board, player)
            mc_update_scores(scores, _board, provided.PLAYERX)
        print scores
        play = get_best_move(board, scores)
        return play


# Test game with the console or the GUI.  Uncomment whichever
# you prefer.  Both should be commented out when you submit
# for testing to save time.
#provided.play_game(mc_move, NTRIALS, False)
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
