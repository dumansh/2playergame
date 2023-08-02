import socket
from env import *
import pickle
from helpers import META_WIDTH, make_packet
from player import Player


class Network:
    def __init__(self, host=HOST, port=PORT):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = host
        self.port = port
        self.addr = (self.server, self.port)

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            print("Cannot connect to the server")

    def send(self, data: bytes) -> bytes:
        try:
            self.client.send(data)
            return self.client.recv(2048)
        except socket.error as e:
            print(e)

    def sendstr(self, msg: str):
        return self.send(msg.encode())

    def send_with_meta(self, meta: str, data: bytes):
        return self.send(make_packet(meta, data))

    def ask_for_opponent(self):
        opponent_info = self.sendstr("OPPONENT")
        meta = opponent_info[:META_WIDTH].decode()
        if "NO_OPPONENT" in meta:
            return
        else:
            opponent = pickle.loads(opponent_info[META_WIDTH:])
            return opponent

    def update(self, player: Player):
        return pickle.loads(self.send_with_meta("MOVE", player.pickle()))


