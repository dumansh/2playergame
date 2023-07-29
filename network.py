import socket
import time
from env import *

class Network:
    def __init__(self, host=HOST, port=PORT):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = HOST
        self.port = PORT
        self.addr = (self.server, self.port)

    def connect(self):
        try:
            self.client.connect(self.addr)
            position_info = self.client.recv(2048).decode()
            return position_info

        except:
            print("Cannot connect to the server")

    def send(self, data: str):
        try:
            self.client.send(data.encode())
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

    def get_pos(self):
        return self.pos


if __name__ == "__main__":
    n = Network()
    received = n.send("hello")
    print(received)
    time.sleep(20)
