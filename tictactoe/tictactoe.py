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
    count = 0
    for row in board:
        for line in row:
            if line == X or line == O:
                count += 1

    # If in middle of game
    count = count % 2
    if count == 0:
        return X
    else:
        return O

    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for k in range(3):
        for i in range(3):
            if board[k][i] == None:
                action = (k, i)
                actions.add(action)
    return actions



    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] != None:
        raise Exception

    newBoard = copy.deepcopy(board)
    newBoard[action[0]][action[1]] = player(board)
    return newBoard


    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # horizontal
    for row in board:
        check = set(row)
        if len(check) == 1:
            winner = list(check)
            if winner[0] != None:
                return winner[0]


    # Vertical
    winner = set()
    for i in range(3):
        for k in range(3):
            winner.add(board[k][i])
        if len(winner) == 1:
            winner = list(winner)
            if winner[0] != None:
                return winner[0]
            else:
                winner = set(winner)
                winner.clear()
        else:
            winner.clear()

    # Diagonal
    if board[0][0] == board[1][1] == board[2][2] or board[0][2] == board[1][1] == board[2][0]:
        if board[1][1] != None:
            return board[1][1]


    return None
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # check for winner
    if winner(board) == None:
        # check if board is filled
        
        for row in board:
            if None in row:
                return False

        return True
        
    else:
        return True
    

    
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == None:
        return 0
    elif winner(board) == 'X':
        return 1
    else:
        return -1

    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None

    if player(board) == 'X':
        values = []
        minScore = 99
        maxScore = -99
        for action in actions(board):
            newBoard = result(board, action)
            values.append(minValue(newBoard,minScore,maxScore))

        for i in range(len(values)):
            if max(values) == values[i]:
                bestAction = list(actions(board))
                bestAction = bestAction[i]
                return bestAction

    elif player(board) == 'O':
        values = []
        maxScore = -99
        minScore = 99
        for action in actions(board):
            newBoard = result(board,action)
            values.append(maxValue(newBoard, minScore,maxScore))

        for i in range(len(values)):
            if min(values) == values[i]:
                bestAction = list(actions(board))
                bestAction = bestAction[i]
                return bestAction




def maxValue(board, minScore, maxScore):
    if terminal(board):
        return utility(board)
    else:
        scores = []
        
        for action in actions(board):
            newBoard = result(board,action)
            score = minValue(newBoard, minScore, maxScore)

            # lowest score possible from this board
            if score > maxScore:
                maxScore = score
            if score > minScore:
                scores.append(score)
                break
        
            scores.append(score)
        return max(scores)



def minValue(board, minScore, maxScore):
    if terminal(board):
        return utility(board)
    else:
        scores = []

        for action in actions(board):
            newBoard = result(board,action)
            score = maxValue(newBoard, minScore, maxScore)

            # get the highest score achievable from this board
            if score < minScore:
                minScore = score
            if score < maxScore:
                scores.append(score)
                break

            scores.append(score)
        return min(scores)
        


    raise NotImplementedError
