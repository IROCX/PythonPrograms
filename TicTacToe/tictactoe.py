
# tic tac toe game
import random

# global vars
game_on = True

# board
board = [' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ' - ', ]

# winner or tie
winner = None

# whose turn
player = 'player'


# display
def display_board():
    print(board[0]+" | " + board[1]+" | "+board[2] + '\n' +
        "--- + --- + ---"+'\n' +
        board[3]+" | " + board[4]+" | "+board[5]+'\n' +
        "--- + --- + --- "+'\n' +
        board[6]+" | " + board[7]+" | "+board[8])

# handle a turn
def handle_turn(player):
    # if turn == 'player':


    if player == 'player' :
        position = input("enter your position (1-9) : ")
        position = int(position)-1
        while board[position]!=' - ':
            position = input("enter valid position : ")
            position = int(position)-1
        board[position] = ' X '
    else:
        cpu_position = int(random.random()*9)
        while board[cpu_position] != ' - ':
            cpu_position = int(random.random()*9)
        board[cpu_position] = ' O '

    display_board()


def check_game_over():
    global winner
    global player
    if check_win():
        winner = player
        return True
    elif check_tie():
        return True
    else:
        return False


def check_win():
    # check rows
    row_winner = check_rows()

    # check cols
    cols_winner = check_cols()

    # check diagonal
    diagonal_winner = check_diagonal()

    return (diagonal_winner or row_winner or cols_winner)


def check_rows():
    if ((board[0] == board[1] == board[2] != ' - ') or
        (board[3] == board[4] == board[5] != ' - ') or
        (board[6] == board[7] == board[8] != ' - ')):
        return True
    else:
        return False


def check_cols():
    if ((board[0] == board[3] == board[6] != ' - ') or
        (board[1] == board[4] == board[7] != ' - ') or
        (board[2] == board[5] == board[8] != ' - ')):
        return True
    else:
        return False


def check_diagonal():
    if ((board[0] == board[4] == board[8] != ' - ') or
        (board[2] == board[4] == board[6] != ' - ')):
        return True
    else:
        return False

def check_tie():
    if ' - ' not in board:
        return True
    else:
        return False


def change_player():
    global player
    if player == 'cpu':
        player = 'player'
    else:
        player = 'cpu'
    return


# play game
def play_game():
    global winner
    global player
    # display board at game start
    display_board()

    while game_on:
        # handle a turn of the player
        handle_turn(player)

        # check if game is over
        if check_game_over():
            break

        # change the player
        change_player()

    # if game ends
    if winner == 'player':
        print('CONGRATS!!! You won.')
    elif winner == 'cpu':
        print('Sorry...CPU won.\nBetter luck next time.')
    else:
        print('Game tied.')


play_game()
