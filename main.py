import pygame
from Network import Packet
from Components import Board, Screens
from Network import Update

from Components.Screen.ScreenManager import ScreenManager


def main():
    screenmanager = ScreenManager()
    screenmanager.set_screen("1", Screens.client_main_menu())
    while screenmanager.check_open():
        screenmanager.draw()
        screenmanager.tick()
    pygame.quit()
    quit()


def click(board, network):
    # Draw the board
    board.board.draw(flip=False)

    # Iterate through the player's pieces
    for piece in board.pieces:
        # If any piece can move on the board, it will move and the player's turn will end.
        # The player's updated game state is then sent over the network using the `network` object.
        if piece.move(board, network):
            board.is_turn = False
            playerobject = Packet.Player(board.side, board.is_turn, board.name)
            playerobject.pieces = board.pieces
            network.send(playerobject)
            break
    else:
        # If no pieces can be moved, the function iterates through the player's pieces again
        # and calls the `click` method on each piece.
        for piece in board.pieces:
            piece.click(board)

    # Finally, the function updates the display.
    pygame.display.flip()


def play(username, ip, port):
    # Create the board and the network
    board, network = Board.setup_board_network(ip, port, username)


    while board.board.check_open():
        # check for updates from server
        # if update returns false then the game is over
        if not Update.update(network, board):
            break

        # check for new clicks on the board
        if board.board.newclick and board.is_turn:
            click(board, network)

    else:
        # else is called if the while check fails (the window is closed)
        network.send(Packet.Quit)
        quit()
    while board.board.check_open():
        pass


if __name__ == "__main__":
    main()
