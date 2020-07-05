from math import inf

HUMAN = 1
COMP = -1

board = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]


def evaluate(state):
    """Perform heuristic evaluation from board"""
    if wins(state, COMP):
        score = -1
    elif wins(state, HUMAN):
        score = 1
    else:
        score = 0

    return score

def empty_cells(state):
    """Extract the remainder of board"""
    cells = []

    for i, row in enumerate(state):
        for j, col in enumerate(row):
            if state[i][j] == 0:
                cells.append([i, j])

    return cells

def wins(state, player):
    """
    Contains all winning condition,
    players is win for sure if their symbols (X or O)
    placed in 3 consecutive lines (horizontal, vertical or diagonal)
    example:

    Three in a row      Three in a diagonal     Three in a col
        [X, X, X]           [O,  ,  ]               [O, X, X]
        [ , O, O]           [X, O,  ]               [O, X,  ]
        [ ,  ,  ]           [X,  , O]               [O,  ,  ]

    """
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]

    if [player, player, player] in win_state:
        return True
    else:
        return False

def game_over(state):
    """Check game over condition"""
    return wins(state, HUMAN) or wins(state, COMP)

def minimax(state, depth, player):
    """
    Minimax implementation for computer moves,
    it recursively traverse the tree to search the
    best possible moves to hinder other players winning move.
    """

    if player == COMP:
        best = [-1, -1, inf]
    else:
        best = [-1, -1, -inf]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] < best[2]:
                best = score
        else:
            if score[2] > best[2]:
                best = score

    return best

def reset_board(state):
    for index in range(3):
        state[index] = [0, 0, 0]