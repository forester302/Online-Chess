import pickle
import socket


class Network:

    packet = None

    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip
        self.port = port
        self.addr = (self.server, self.port)
        self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            self.packet = pickle.loads(self.client.recv(4096))
        except Exception as e:
            print(e)

    def get_packet(self):
        return self.packet

    def send(self, object_):
        try:
            self.client.send(pickle.dumps(object_))
            self.packet = pickle.loads(self.client.recv(4096))
        except Exception as e:
            print(e)
