#Milan Patel and Faizan Rashid
import connectfour
import common_functions 
       

def want_to_play()-> None:
    """introduces user and asks them if they want to start a new game"""
    common_functions.welcome_message()
    yes_or_no = str(input('Would you like to start a new game? (Enter Y or N) '))
    #user has to enter Y or N (lowercase or uppercase) or keep asking
    while yes_or_no.lower().strip() != 'y' and yes_or_no.lower().strip() != 'n':
        print('\nPlease enter Y or N')
        yes_or_no = str(input('\nWould you like to start a new game? (Enter Y or N) '))
    #if they say yes, call function that executes game
    if yes_or_no.lower().strip() == 'y':
        print()
        print('Enjoy your game!\n')
        play_game()
    elif yes_or_no.lower().strip() == 'n':
        print('You chose not to play. Have a nice day')
        

def play_game():
    """Executes game by using functions from connectfour and common_functions module"""
    #game_status is the GameState
    #call new_game function from connectfour module to create new gamestate
    #then call all functions from the common functions module to play the game
    game_status = connectfour.new_game()
    while True:
        #print current board, get move type, column number, and execute move
        common_functions.print_board(game_status)
        print(common_functions.whose_turn(game_status))
        drop_or_pop = common_functions.choose_move()
        what_column = common_functions.column_number()
        if drop_or_pop == 'DROP':
            game_status = common_functions.move_DROP(game_status, what_column)
        elif drop_or_pop == 'POP':
            game_status = common_functions.move_POP(game_status, what_column)
        #if there is a winner, print winner and end program
        if common_functions.game_win(game_status) == False:
            common_functions.who_wins(game_status)
            break
        else:
            print()
        
        

if __name__ == '__main__':
    want_to_play()

