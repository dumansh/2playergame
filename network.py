import socket
import time
from env import *
import pickle

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

    def send(self, data: bytes)->bytes:
        try:
            self.client.send(data)
            return self.client.recv(2048)
        except socket.error as e:
            print(e)


if __name__ == "__main__":
    n = Network()
    received = n.send("hello")
    print(received)
    time.sleep(20)
