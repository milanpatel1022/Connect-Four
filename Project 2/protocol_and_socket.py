#Milan Patel and Faizan Rashid
#implements the server protocol and all socket handling
#deals with connecting, reading, writing, etc. via a socket. Nothing more.
#server is ron-cadillac.ics.uci.edu
#port is 4444

from collections import namedtuple
import socket


GameConnection = namedtuple(
    'GameConnection',
    ['socket', 'socket_in', 'socket_out'])


class GameProtocolError(Exception):
    pass


def connect(host: str, port: int) -> GameConnection:
    """Attempts to connect to host and port that are given by user"""
    game_socket = socket.socket()
    try:
        game_socket.connect((host, port))
        socket_input = game_socket.makefile('r')
        socket_output = game_socket.makefile('w')
    #If host is not valid then error is raised
    except socket.gaierror:
        print('Connection to host failed')
    else:
        return GameConnection(
        socket = game_socket,
        socket_in = socket_input,
        socket_out = socket_output)


def close_socket(connection: GameConnection) -> None:
    """Closes connection to server"""
    connection.socket_in.close()
    connection.socket_out.close()
    connection.socket.close()


def hello(connection: GameConnection, username: str) -> bool:
    """Checks if server sends correct response to protocol and valid username given by user"""
    _write_line(connection, f'I32CFSP_HELLO {username}')

    response = _read_line(connection)

    if response == ('WELCOME %s' %username):
        return True
    elif response.startswith('NO_USER '):
        print('No existing user')
        return False
    else:
        raise GameProtocolError()


def ask_game(connection: GameConnection, requestgame: str) -> bool:
    """Checks if server has correct response to 'AI_GAME' if user wants to play a game"""
    if requestgame == 'y':
        _write_line(connection, f'AI_GAME')
        response = _read_line(connection)
        if response == 'READY':
            return True
    elif requestgame != 'y':
        print('You chose not to play')


def play_game(connection: GameConnection, drop_or_pop: str, what_column: int) -> str:
    """Checks if each line of the server's response is valid following a move by the user"""
    move = '%s %d' % (drop_or_pop, what_column)
    _write_line(connection, move)
    first_line = _read_line(connection)
    if first_line == 'OKAY':
        AI_move = _read_line(connection)
        ready_or_not = _read_line(connection)
        if ready_or_not == 'READY' or ready_or_not == 'WINNER_RED' or ready_or_not == 'WINNER_YELLOW':
            return AI_move
        else:
            close_socket(connection)
            



def _write_line(connection: GameConnection, line: str) -> None:
    """Sends user's move to server"""
    connection.socket_out.write(line + '\r\n')
    connection.socket_out.flush()


def _read_line(connection: GameConnection) -> str:
    """Reads a line from server's response"""
    line = connection.socket_in.readline()[:-1]
    return line
