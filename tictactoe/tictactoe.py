"""
Tic Tac Toe Player
"""

import math
import copy

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
    x_count = 0
    y_count = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == X:
                x_count += 1
            elif board[i][j] == O:
                y_count += 1
    
    return X if x_count <= y_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    result = set()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == EMPTY:
                result.add((i, j))
    return result


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    if i < 0 or j < 0 or i >= len(board) or j >= len(board[0]) or board[i][j] != EMPTY:
        raise Exception
    
    result_board = copy.deepcopy(board)
    result_board[action[0]][action[1]] = player(board)
    return result_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check rows
    for i in range(len(board)):
        if not any(cell != X for cell in board[i]):
            return X
        elif not any(cell != O for cell in board[i]):
            return O
    # check columns
    for j in range(len(board[0])):
        if board[0][j] == board[1][j] == board[2][j] == X:
            return X
        elif board[0][j] == board[1][j] == board[2][j] == O:
            return O
    # check diagonal top to bottom
    if board[0][0] == board[1][1] == board[2][2] == X:
        return X
    elif board[0][0] == board[1][1] == board[2][2] == O:
        return O
    
    # check diagonal bottom to top
    if board[2][0] == board[1][1] == board[0][2] == X:
        return X
    elif board[2][0] == board[1][1] == board[0][2] == O:
        return O
    
    # no winner / tie
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # game is over if there is a winner
    if winner(board):
        return True
    # game is not over if there is an empty cell
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == EMPTY:
                return False
    # game is over if there are no empty cells and no winner
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # assume the board is terminal
    game_winner = winner(board)
    if game_winner == X:
        return 1
    elif game_winner == O:
        return -1
    else:
        return 0
    

def get_max_value(board):
    v = float('-inf')
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v, get_min_value(result(board, action)))
    return v


def get_min_value(board):
    v = float('inf')
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v, get_max_value(result(board, action)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # if the game is over, there is no next move
    if terminal(board):
        return None
    # if the current player is X, maximize the result
    # otherwise, minimize the result
    available_moves = list(actions(board))
    # default to the first available move if there is no best move
    best_move = available_moves[0]
    first_player = player(board)
    # initialize the best score given the first player
    if first_player == X:
        best_score = float('-inf')
    else:
        best_score = float('inf')

    if first_player == X:
        for move in available_moves:
            # to maximize the score, get the min
            score = get_min_value(result(board, move))
            if score > best_score:
                best_score = score
                best_move = move
    else:
        for move in available_moves:
            # to minimize the score, get the max
            score = get_max_value(result(board, move))
            if score < best_score:
                best_score = score
                best_move = move
    return best_move


# if __name__ == "__main__":
#     # Get command line arguments
#     import sys
#     # arg1 = sys.argv[1]
    
#     # Call the method with command line arguments
#     board = initial_state()
#     board[0][0] = X
#     board[1][0] = O
#     board[0][1] = X
#     board[1][1] = X
#     board[0][2] = O
#     board[1][2] = X
#     board[2][2] = O
#     print(minimax(board))

'''
X, X, O
O, X, X
None, None, O
res = (2,1)
'''
