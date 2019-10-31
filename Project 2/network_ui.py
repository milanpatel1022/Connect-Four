#Milan Patel & Faizan Rashid

import connectfour
import protocol_and_socket
import common_functions

def run_user_interface() -> None:
    """Gets user input needed to connect to the server and calls game function if server responds correctly"""
    #Introduce user & ask for server name, port and username
    common_functions.welcome_message()
    host = _read_host()
    port = _read_port()
    user = _user_name()
    #call functions from protocol and socket module with given info to attempt connection
    connection = protocol_and_socket.connect(host, port)
    if connection != None:
        #if server's response is correct, continue
        if protocol_and_socket.hello(connection, user) == True:
            want_to_play = protocol_and_socket.ask_game(connection, _request_game())
            if want_to_play == True:
                print('\nEnjoy your game! (AI will assume the YELLOW player)\n')
                ui_game(connection)

def ui_game(connection):
    """Executes game by calling functions from connectfour, common_functions and protocol_and_sockets modules"""
    game_status = connectfour.new_game()
    connection_response = None
    while True:
        common_functions.print_board(game_status)

        
        #Loop for USER'S TURN
        if common_functions.whose_turn(game_status) == "\nRED'S TURN":
            print(common_functions.whose_turn(game_status))
            drop_or_pop = common_functions.choose_move()
            what_column = common_functions.column_number()
            #store the server's response for later use
            connection_response = protocol_and_socket.play_game(connection, drop_or_pop, what_column)
            game_status = _execute_server_move(game_status, drop_or_pop, what_column)


        #Loop for AI'S TURN       
        elif common_functions.whose_turn(game_status) == "\nYELLOW'S  TURN":
            print("\n\nYELLOW'S TURN... YELLOW MADE MOVE")
            
            drop_pop_or_winner, what_column = _server_response(connection_response)

            if _check_response(drop_pop_or_winner, what_column) != False:
               game_status = _execute_server_move(game_status, drop_pop_or_winner, what_column)

        #check for winner, False if there is a winner. If False then call who_wins function to find who the winner is
        if common_functions.game_win(game_status) == False:
            common_functions.who_wins(game_status)
            protocol_and_socket.close_socket(connection)
            break
        else:
            print()
        
         

def _server_response(response:str):
    """Splits the AI's move into its move choice (drop or pop) and column number"""
    move_choices = response.split(' ')
    drop_pop_or_winner = move_choices[0]
    what_column = int(move_choices[1])
    return drop_pop_or_winner, what_column


def _check_response(drop_pop_or_winner: str, what_column: int) -> bool:
    """if the server's response did not include 'DROP' or 'POP' or 'WINNER' or a valid column number, close the connection to server"""
    if drop_pop_or_winner != 'DROP' and drop_pop_or_winner != 'POP' and drop_pop_or_winner != 'WINNER_RED' and drop_pop_or_winner != 'WINNER_YELLOW':
        protocol_and_socket.close_socket(connection)
        return False
    #if the server's column choice was not within the range of the board, close the connection to server
    if what_column > connectfour.BOARD_COLUMNS or what_column < 1:
        protocol_and_socket.close_socket(connection)
        return False


def _execute_server_move(game_status, drop_pop_or_winner: str, what_column: int) -> tuple:
    """Executes drop or pop move depending on AI's response"""
    if drop_pop_or_winner == 'DROP':
        game_status = common_functions.move_DROP(game_status, what_column)
    elif drop_pop_or_winner == 'POP':
        game_status = common_functions.move_POP(game_status, what_column)
    elif drop_pop_or_winner == 'WINNER_RED' or 'WINNER_YELLOW':
        pass
    return game_status


def _read_host() -> str:
    """Gets valid host from user"""
    while True:
        host = input('Host: ').strip()
        if host != '':
            return host
        else:
            print('Not a valid host; try again!')
            

def _user_name() -> str:
    """Gets valid username from user"""
    user = input('User: ').strip()
    while ' ' in user or len(user) == 0:
        print('Invalid username; try again!')
        user = input('User: ').strip()
    return user


def _read_port() -> int:
    """Gets valid port from user"""
    port = input('Port: ')
    while port.isdigit() == False or int(port) < 0 or int(port) > 65535 or ' ' in port:
        print('Not a valid port; must be a number from 0-65535; try again!')
        port = input('Port: ')
    return int(port)


def _request_game() -> str:
    """Asks the user if they want to play a game with the AI or not"""
    ready = input('\nDo you want to play a game? (Y or N) ')
    while ready.strip().lower() != 'y' and ready.strip().lower() != 'n':
        print('\nEnter Y or N')
        ready = input('\nDo you want to play a game? (Y or N) ')
    return ready.lower()
        


    
if __name__ == '__main__':
    run_user_interface()
                
