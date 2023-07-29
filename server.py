import socket
import _thread
import sys
from env import *
from typing import Tuple
import color

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((HOST, PORT))

except socket.error as e:
    print(str(e))
    exit(1)

s.listen(2)  # max 2 connection
print("Server started")


class PlayerData:
    def __init__(self, player_id, color_str, x, y, joined=False):
        self.player_id = player_id
        self.color_str=color_str
        self.posX=x
        self.posY=y
        self.joined=joined

    def __repr__(self):
        return str(self.player_id) + ", " + self.color_str + ", " + str(self.posX) + ", " + str(self.posY)

    def opponent_id(self):
        return 3 - self.player_id

    def update(self, client_data: Tuple[str, str, str, str]):
        self.posX = client_data[3]
        self.posY = client_data[4]

p1=PlayerData(1, "RED", 100, 50)
p2=PlayerData(2, "BLUE", 300, 200)
players = [p1, p2]


active_connections = []

player_count=0
def thread_client(conn):
    global players
    player=None
    for p in players:
        if not p.joined:
            p.joined = True
            player = p
            break
    if not player:
        conn.send("Already 2 players".encode())
        conn.close()
    else:
        handshake_sig = str(player)
        conn.send(handshake_sig.encode())


    while True:
        try:
            data = conn.recv(2048).decode("utf-8")

            if not data:
                print("No data remaining to read")
                break
            else:

                if data=="OPPONENT":
                    print("trying to find the opponent")
                    opponent=players[player.opponent_id()- 1]
                    if opponent.joined:
                        print("Opponent had joined")
                        conn.sendall(str(opponent).encode())
                    else:
                        print("Opponent has not joined")
                        conn.sendall("NO_OPPONENT".encode())
                data_tuple = data.split(", ")
                if data_tuple[0] == "MOVE":
                    player.update(data_tuple)
                    conn.send(str(opponent).encode())

        except Exception as e:
            print(e)
            break

    print("Lost connection")
    if player:
        player.joined=False
    conn.close()



if __name__ == "__main__":
    while True:
        try:
            conn, addr = s.accept()
            print("Connected to ", addr)
            _thread.start_new_thread(thread_client, (conn,))
        except KeyboardInterrupt:
            print("keyboard Inturrupt handled by except block")
            exit(0)
