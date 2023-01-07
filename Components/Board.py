import pygrille

import Network.Packet, Network.Network
from Components.Piece.piece import King, Rook, Queen, Bishop, Knight


class Board:
    def __init__(self):
        # initialize variables for storing pieces on the board
        self.pieces = None
        self.otherpieces = None
        self.king: King = None
        self.is_turn = True
        self.side: int = None
        self.name: str = None

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
    for piece in board.pieces + board.otherpieces:
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


def promotion(pawn, board: Board, network: Network):
    from Network import Update
    board.board.set_ui("promote", "images/promotion.png", (75, 225), (451, 151))

    pieces = {
        2: Rook((2, 4), pawn.d),
        3: Knight((3, 4), pawn.d),
        4: Bishop((4, 4), pawn.d),
        5: Queen((5, 4), pawn.d)
    }

    pieces2 = board.pieces
    pieces3 = board.otherpieces

    board.pieces = list(pieces.values())
    board.otherpieces = []

    place_pieces(board)

    while board.board.check_open():
        # check for updates from server
        # if update returns false then the game is over
        if not Update.update(network, board):
            break

        # check for new clicks on the board
        if board.board.newclick:
            lastclick = board.board.lastclick
            if 2 <= lastclick[0] <= 5 and lastclick[1] == 4:
                piece = pieces[lastclick[0]]
                piece.x = pawn.x
                piece.y = pawn.y

                pieces2.remove(pawn)
                pieces2.append(piece)

                board.pieces = pieces2
                board.otherpieces = pieces3

                board.board.del_ui("promote")
                place_pieces(board)
                return

    else:
        # else is called if the while check fails (the window is closed)
        network.send(Network.Packet.Quit)
        quit()
    while board.board.check_open():
        pass
