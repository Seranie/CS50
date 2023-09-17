import tictactoe as ttt

X = "X"
O = "O"
EMPTY = None

def main():
    board = [
        [EMPTY,EMPTY,EMPTY],
        [X,EMPTY,EMPTY],
        [EMPTY,EMPTY,EMPTY]
    ]
    
    while True:
        if ttt.terminal(board):
            print(ttt.winner(board))
            break
        bestMove = ttt.minimax(board)
        currentPlayer = ttt.player(board)
        board[bestMove[0]][bestMove[1]] = currentPlayer
        

main()