import pickle
import socket
from _thread import start_new_thread
# Initialize server address and port
from Components import Screens
from Components.Screen.ScreenManager import ScreenManager
from Network import Packet

server = "0.0.0.0"
port = 5555  # input("Enter The Port The Server Should Run On: ")

# Try to convert user input to integer and set default port if invalid
try:
    port = int(port)
    # Set port to maximum value if too large
    if port > 65535:
        port = 65535
    # Set port to minimum value if too small
    if port <= 0:
        port = 1
# Set default port if input cannot be converted to integer
except ValueError:
    port = 5555

# Create a TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Try to bind the socket to the server address and port
try:
    s.bind((server, port))
# Catch and print any errors that occur
except socket.error as e:
    print(e)

# Put the socket into listening mode
s.listen()

# Print a message indicating the server is ready to accept connections
print(f"Waiting for a connection, Server Started on {socket.gethostbyname(socket.gethostname())}:{port}")

pieces = [Packet.Player(1, False), Packet.Player(-1, False)]
updates = [pieces[0], pieces[1]]
for piece in pieces:
    piece.gen_pieces()
update = -1


def save_to_file(id):
    with open(f"Saves/save{id}.chess", "wb") as save:
        pickle.dump(pieces, save)


def load_from_file(id):
    global pieces
    with open(f"Saves/save{id}.chess", "rb") as save:
        pieces = pickle.load(save)


def pygame_thread(ip, port):
    screenmanager = ScreenManager()
    screenmanager.set_screen("run", Screens.server_running_menu(ip, screenmanager, save_to_file))
    while screenmanager.check_open():
        screenmanager.draw()
        screenmanager.tick()


def threaded_connection(conn, *args):
    global update, players  # Needed to modify global variables

    def on_update_request(update, just_joined):
        """Handle requests for updates to the game state."""
        if update == replyid:  # Other player made a update
            reply = updates[replyid]  # Send updated game state
            update = -1  # Reset update
        elif just_joined:  # Player has just joined, send current game state
            reply = pieces[replyid]
            # deal with player reconnecting
            updates[side] = pieces[side]
            update = side
            just_joined = False
        else:  # No update to game state
            reply = Packet.NoUpdatesAvailable()

        return update, just_joined, reply

    def on_update_game_state(data):
        """Handle updates to the game state."""
        if isinstance(data, Packet.Player):
            pieces[side] = data
        updates[side] = data
        update = side  # Update made by current player
        reply = Packet.NoUpdatesAvailable()
        return update, reply

    print("thread started")
    conn.send(pickle.dumps(Packet.UsernameRequest()))
    data = pickle.loads(conn.recv(4096))
    if isinstance(data, Packet.Username):
        username = data.name
        for i, player in enumerate(pieces):
            if player.name == username:
                side = i
                break
            elif player.name is None:
                side = i
                player.name = username
                break
            # side = 0 for first player, side = 1 for second player
    else:
        conn.send(pickle.dumps(Packet.UsernameDenied()))
        conn.close()
        return

    # Set replyid based on side. replyid is the player ID of the other player.
    if side == 0:
        replyid = 1
    else:
        replyid = 0
        update = 1  # First player has joined, so update is set to 1

    conn.send(pickle.dumps(pieces[side]))  # Send current game state to new player

    just_joined = False
    if players >= 2:
        just_joined = True

    while True:
        try:
            data = pickle.loads(conn.recv(4096))  # Receive data from client
            if data is None:  # Connection closed
                print("Disconnected")
                break
            elif isinstance(data, Packet.UpdateRequest):  # Client requesting an update
                update, just_joined, reply = on_update_request(update, just_joined)
            else:  # Client sent updated game state
                update, reply = on_update_game_state(data)
            conn.sendall(pickle.dumps(reply))  # Send reply to client
        except Exception as e:
            print(e)
            break

    print("Lost connection")
    conn.close()
    players -= 1


# Accept and handle incoming connections indefinitely
#load_from_file(0)
start_new_thread(pygame_thread, (server, port))
players = 0
while True:
    # Accept a new connection
    conn, addr = s.accept()
    # Print the client address of the connection
    print(f"Connected to: {addr}")
    start_new_thread(threaded_connection, (conn, 0))
    players += 1
