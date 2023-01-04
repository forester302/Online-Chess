from Components import Board
from Components.Popup import popups
from Network import Network, Packet


def end_game(packet: Packet.EndGame, board: Board):
    if packet.type == "Checkmate":
        popups["WinCheckmate"].popup(board)
        return False
    elif packet.type == "Stalemate":
        popups["Stalemate"].popup(board)
        return False


def other_player_quit(board):
    board.otherpieces = []
    Board.place_pieces(board)
    return True


def other_player_check():
    print("You Checked The Opponent")
    return True


def update_game_state(packet: Packet.Player, board: Board.Board, network: Network.Network):
    # Set the current player's turn to True.
    board.is_turn = not packet.is_turn

    # Sync the current player's pieces with the server's pieces.
    # This involves looping through the server's pieces and deleting
    # the corresponding pieces from the current player's pieces if
    # a piece has been taken (if it has been captured in a chess move).
    for piece in packet.pieces:
        for i in range(0, len(board.pieces)):
            piece2 = board.pieces[i]
            if piece.x == 7 - piece2.x and piece.y == 7 - piece2.y:
                board.pieces.pop(i)
                break

    # Store the other player's pieces in board.otherpieces and reverse their
    # x and y coordinates.
    board.otherpieces = packet.pieces
    for piece in packet.pieces:
        piece.y = 7 - piece.y
        piece.x = 7 - piece.x

    # Update the game board with the new positions of the pieces.
    Board.place_pieces(board)

    # check for check
    if board.king.is_in_check(board, (-1, -1)):
        # check for checkmate
        moves = []
        for piece in board.pieces:
            moves += piece.possible_moves(board)
            if len(moves) > 0:
                popups["Check"].popup(board)
                break
        else:
            popups["Checkmate"].popup(board)
            network.send(Packet.EndGame("Checkmate"))
            return False
    else:
        # check for stalemate
        moves = []
        for piece in board.pieces:
            moves += piece.possible_moves(board)
            if len(moves) > 0:
                break
        else:
            popups["Stalemate"].popup(board)
            network.send(Packet.EndGame("Stalemate"))
            return False
    return True


def update(network: Network.Network, board: Board):
    # Send a message to the server indicating that we are ready for an update.
    network.send(Packet.UpdateRequest())

    # Receive a message from the server.
    packet = network.get_packet()

    # If we did not receive a packet, then the connection must have been closed.
    # In this case, we exit the loop.
    if packet is None:
        return False

    if isinstance(packet, Packet.EndGame):
        return end_game(packet, board)

    if isinstance(packet, Packet.Quit):
        return other_player_quit(board)

    if isinstance(packet, Packet.Check):
        return other_player_check

    # If the data we received is an instance of the Player class, then it represents
    # the other player's latest game state.
    if isinstance(packet, Packet.Player):
        return update_game_state(packet, board, network)

    return True
