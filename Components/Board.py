import pygrille

import Network.Packet, Network.Network
from Components.Piece.piece import King


class Board:
    # initialize variables for storing pieces on the board
    pieces = None
    otherpieces = None
    king: King = None
    is_turn = True
    side: int = None
    name: str = None

    def __init__(self):
        # initialize the board and draw it to the screen
        self.board = gen_board()


def gen_board():
    # helper function to invert the color
    def invert_colour(colour):
        if colour == (0, 0, 0):
            return (255, 255, 255)
        else:
            return (0, 0, 0)

    # create a grid using the pygrille library
    # the grid is 8x8 cells with a border width of 2 and a border color of (70,70,70)
    # the frame rate is set to 20 and the window is named "chess"
    grid = pygrille.Grid(73, (8, 8), border_width=2, border_colour=(70, 70, 70), framerate=20, window_name="chess")

    # set the initial color to white
    colour = (255, 255, 255)

    # loop through the cells in the grid and set the color
    # the color alternates between white and black
    for i in range(0, 8):
        for j in range(0, 8):
            grid[i][j].colour = colour
            colour = invert_colour(colour)
        colour = invert_colour(colour)

    # draw the grid to the screen
    grid.draw()

    # return the grid
    return grid


# function to place pieces on the board
def place_pieces(board):
    # clear all previous pieces from the board
    for row in board.board.grid:
        for square in row:
            square.image = None
    # place the current pieces down in the correct positions
    for piece in board.pieces:
        piece.place_piece(board)
    for piece in board.otherpieces:
        piece.place_piece(board)
    # draw the board
    board.board.draw()


def setup_board_network(ip: str, port: int, username: str):
    network = Network.Network.Network(ip, port)
    packet = network.get_packet()
    if isinstance(packet, Network.Packet.UsernameRequest):
        network.send(Network.Packet.Username(username))
    else:
        print(packet)
        quit("Not a Server")
    player = network.get_packet()
    if isinstance(player, Network.Packet.UsernameDenied):
        quit("Username Denied")

    # create an instance of the Board class and generate the board
    board = Board()

    board.side = player.side
    board.name = player.name

    board.is_turn = player.is_turn

    # assign pieces to the board
    board.king = player.pieces[0]
    board.pieces = player.pieces
    board.otherpieces = []

    # place the pieces on the board
    place_pieces(board)

    return board, network
