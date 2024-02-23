"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    Xs = 0
    Os = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                Xs += 1
            elif board[i][j] == O:
                Os += 1

    if Xs == 0 and Os == 0:
        return X
    elif Xs == Os:
        return X
    else:
        return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    res = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                res.add((i, j))
    
    return res

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    res = [row[:] for row in board]
    i, j = action
    if res[i][j] != EMPTY:
        raise Exception("Invalid move")
    else:
        res[i][j] = player(board)

    return res

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if board[i][0] == board[i][1] and board[i][1] == board[i][2]:
            return board[i][0]

        elif board[0][i] == board[1][i] and board[1][i] == board[2][i]:
            return board[0][i]

    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[0][0]
    
    if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        return board[0][2]
    
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    res = True
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                res = False
    if utility(board) == 1 or utility(board) == -1:
        res = True
    return res

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    res = 0
    if winner(board) == O:
        res = -1
    elif winner(board) == X:
        res = 1
    return res


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    if player(board) == X:
        _, action = max_value(board)
    else:
        _, action = min_value(board)

    return action

def max_value(board):
    """
    Returns the maximum utility value and corresponding action for X.
    """

    if terminal(board):
        return utility(board), None
    
    v = -1
    best_action = None

    for action in actions(board):
        new_v, _ = min_value(result(board, action))
        if new_v > v:
            v = new_v
            best_action = action
        if v == 1: # alpha-beta prunning
            return v, best_action

    return v, best_action

def min_value(board):
    """
    Returns the minimum utility value and corresponding action for O.
    """
    if terminal(board):
        return utility(board), None

    v = 1
    best_action = None

    for action in actions(board):
        new_v, _ = max_value(result(board, action))
        if new_v < v:
            v = new_v
            best_action = action
        if v == -1: # alpha-beta prunning
            return v, best_action

    return v, best_action

