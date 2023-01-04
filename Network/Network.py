import pickle
import socket


class Network:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    packet = None

    def __init__(self, ip, port):
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

    def send(self, object):
        try:
            self.client.send(pickle.dumps(object))
            self.packet = pickle.loads(self.client.recv(4096))
        except Exception as e:
            print(e)
