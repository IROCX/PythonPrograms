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

    print('\n')

# handle a turn


def handle_turn(player):

    if player == 'player':
        position = input("Enter your position (1-9) : ")

        while True:
            try:
                position = int(position)-1
                break
            except ValueError:
                position = input("Enter a numeric position (1-9) : ")

        while (not (0 <= position < 9)):
            position = input("Enter valid position (1-9) : ")
            position = int(position)-1

        while board[position] != ' - ':
            position = input("Already occupied. Enter valid position : ")
            position = int(position)-1

        board[position] = ' X '
    else:
        cpu_position = cpu_move()

        if cpu_position == -1:
            print('Game tied.')
            return
        else:
            # cpu_position = int(random.random()*9)
            # while board[cpu_position] != ' - ':
            #     cpu_position = int(random.random()*9)
            board[cpu_position] = ' O '

    display_board()


def cpu_move():
    global board
    possible_moves = [x for x, letter in enumerate(board) if letter == ' - ']
    move = -1
    print(list(enumerate(board)))
    print(possible_moves)

    for let in [' O ', ' X ']:
        for i in possible_moves:
            boardCopy = board[:]
            boardCopy[i] = let
            print(boardCopy[0]+" | " + boardCopy[1]+" | "+boardCopy[2] + '\n' +
                  "--- + --- + ---"+'\n' +
                  boardCopy[3]+" | " + boardCopy[4]+" | "+boardCopy[5]+'\n' +
                  "--- + --- + --- "+'\n' +
                  boardCopy[6]+" | " + boardCopy[7]+" | "+boardCopy[8])
            print(check_win(boardCopy))
            print()

    if check_win(boardCopy):
        print('winnig move detected', i)
        move = i
        return move

    cornersOpen = []
    for i in possible_moves:
        if i in [0, 2, 6, 8]:
            cornersOpen.append(i)

    if len(cornersOpen) > 0:
        move = cornersOpen[int(random.random()*(len(cornersOpen)-1))]
        print('corner move detected', move)
        return move

    if 4 in possible_moves:
        move = 5
        return move

    edgesOpen = []
    for i in possible_moves:
        if i in [1, 3, 5, 7]:
            edgesOpen.append(i)

    if len(edgesOpen) > 0:
        move = cornersOpen[int(random.random()*(len(edgesOpen)-1))]
        print('edge move detected', move)
        return move

    return move


def check_game_over():
    global winner
    global player
    global board
    if check_win(board):
        winner = player
        return True
    elif check_tie(board):
        return True
    else:
        return False


def check_win(b):
    # check rows
    row_winner = check_rows(b)

    # check cols
    cols_winner = check_cols(b)

    # check diagonal
    diagonal_winner = check_diagonal(b)

    return (diagonal_winner or row_winner or cols_winner)


def check_rows(board):
    if ((board[0] == board[1] == board[2] != ' - ') or
        (board[3] == board[4] == board[5] != ' - ') or
            (board[6] == board[7] == board[8] != ' - ')):
        return True
    else:
        return False


def check_cols(board):
    if ((board[0] == board[3] == board[6] != ' - ') or
        (board[1] == board[4] == board[7] != ' - ') or
            (board[2] == board[5] == board[8] != ' - ')):
        return True
    else:
        return False


def check_diagonal(board):
    if ((board[0] == board[4] == board[8] != ' - ') or
            (board[2] == board[4] == board[6] != ' - ')):
        return True
    else:
        return False


def check_tie(board):
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
