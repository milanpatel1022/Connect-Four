#Milan Patel and Faizan Rashid

import connectfour


def print_board(game_status):
    """Prints the board with its current game state"""
    #prints out the board according to # of columns and rows given
    #print number of columns on top of board
    print()
    x = 1
    while x <= connectfour.BOARD_COLUMNS:
        print(x, end= '  ')
        x += 1
    print()
    #make the nested for loop loop through the columns since they need to be printed out first
    #then the outer loop loops through the rows since they need to printed on new lines
    for row in range(connectfour.BOARD_ROWS):
        for col in range(connectfour.BOARD_COLUMNS):
            #print '.', 'R', or 'Y' in each spot on board depending on if a piece was placed
            #and by who
            if game_status.board[col][row] == connectfour.NONE:
                print('.  ', end='')
            elif game_status.board[col][row] == connectfour.RED:
                print('R  ', end='')
            elif game_status.board[col][row] == connectfour.YELLOW:
                print('Y  ', end='')
        #after every row in column is looped through, print line to separate the rows
        print()


def whose_turn(game_status) -> str:
    """Returns whoever's turn it is"""
    if game_status.turn == connectfour.RED:
        one = ("\nRED'S TURN")
        return one
    elif game_status.turn == connectfour.YELLOW:
        two = ("\nYELLOW'S  TURN")
        return two


def choose_move() -> str:
    """Asks user for input on what move they would like to make and returns move. (Must be drop or pop, and it is case insensitive)"""
    #ask user to choose to drop or pop & return input
    what_move = str(input('\nDo you want to DROP or POP a piece? '))
    while what_move.upper().strip() != 'DROP' and what_move.upper().strip() != 'POP':
        print("\nPlease enter 'DROP' or 'POP'\n")
        what_move = str(input('Do you want to DROP or POP a piece? '))
    return what_move.strip().upper()


def column_number() -> int:
    """Asks user for column number until a valid one is given and returns it."""
    #ask user to choose what column to drop or pop & return input
    col_num = input('\nFrom what column? (1 - %s) ' %connectfour.BOARD_COLUMNS)
    while col_num.isdigit() == False or int(col_num) < 1 or int(col_num) > connectfour.BOARD_COLUMNS:
        print('\nInvalid move. Choose a valid column number\n')
        col_num = input('From what column? (1 - %s) ' %connectfour.BOARD_COLUMNS)
    return int(col_num)


def move_DROP(game_status, what_column: int):
    """Executes drop move and checks for possible errors that might occur when 'dropping'"""
    #if the imported drop function raises an error, except is called. Else, update GameState and check for winner
    try:
        return connectfour.drop(game_status, what_column -1)
    #exception for when column is full
    except connectfour.InvalidMoveError:
        print('\nINVALID COLUMN CHOICE.')
        return game_status
    except connectfour.GameOverError:
        print('The game is over. Run the program again if you want to play again!')
        

def move_POP(game_status, what_column: int):
    """Executes the pop move and checks for possible errors that might occur when 'popping'"""
    #if the imported pop function raises an error, except is called. Else, update GameState and check for winner
    try:
        return connectfour.pop(game_status, what_column-1)
    #if the bottom piece in column doesn't belong to the current player's turn, or if the column is empty, move is invalid
    except connectfour.InvalidMoveError:
        print('\nINVALID COLUMN CHOICE. IT IS EMPTY OR THE PIECE AT THE BOTTOM IS NOT YOURS.')
        return game_status
    except connectfour.GameOverError:
        print('The game is over. Run the program again if you want to play again!')


def game_win(game_status) -> bool:
    """This function is called after every move is made & checks if the game has a winner"""
    who_won = connectfour.winner(game_status)
    if who_won == connectfour.RED or who_won == connectfour.YELLOW:
        return False
    else:
        return True


def who_wins(game_status) -> None:
    """Checks who the winner is if there is a winner"""
    if connectfour.winner(game_status) == connectfour.RED:
        print_board(game_status)
        print("\nRED wins!")
    elif connectfour.winner(game_status) == connectfour.YELLOW:
        print_board(game_status)
        print("\nYELLOW wins!")
    

def welcome_message():
    print('Welcome to a game of Connect Four')
    print('---------------------------------')
