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
    # redraw the board
    board.board.draw(flip=False)
    # check if any pieces have been clicked
    for piece in board.pieces:
        if piece.move(board):
            board.is_turn = False
            playerobject = Packet.Player(board.side, board.is_turn, board.name)
            playerobject.pieces = board.pieces
            network.send(playerobject)
            break
    else:
        for piece in board.pieces:
            piece.click(board)
    # update the display
    pygame.display.flip()


def play(username, ip, port):
    # Create the board and the network
    board, network = Board.setup_board_network(ip, port, username)

    # create main loop
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