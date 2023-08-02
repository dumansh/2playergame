import socket
import _thread
from env import *
import pickle
from player import Player

from helpers import META_WIDTH, make_packet

p1 = Player(1, color_str="RED", x=100, y=50)
p2 = Player(2, color_str="BLUE", x=300, y=200)
players = [p1, p2]


def select_player():
    player = None
    for p in players:
        if not p.joined:
            p.joined = True
            player = p
            break
    return player


def find_opponent(player: Player):
    return players[player.opponent_id() - 1]


active_connections = []

player_count = 0


def thread_client(conn):
    run = True
    player = select_player()
    if not player:
        conn.send("Already 2 players".encode())
        run = False
    else:
        conn.send(player.pickle())

    while run:
        try:
            data = conn.recv(2048)
            instruction = data[:META_WIDTH].decode()
            if not data:
                print("No data remaining to read")
                break
            else:

                if "OPPONENT" in instruction:
                    opponent = find_opponent(player)
                    if opponent.joined:
                        packet = make_packet("OPPONENT", opponent.pickle())
                        conn.sendall(packet)
                    else:
                        conn.sendall("NO_OPPONENT".encode())
                        continue

                if "MOVE" in instruction:
                    player.update(pickle.loads(data[META_WIDTH:]))
                    packet = opponent.pickle()
                    conn.send(packet)

        except Exception as e:
            print(e)
            break

    print("Lost connection")
    if player:
        player.joined = False
    conn.close()


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((HOST, PORT))
    except socket.error as e:
        print(str(e))
        exit(1)

    s.listen(2)
    while True:
        print("Server running")
        conn, addr = s.accept()
        print("Connected to ", addr)
        _thread.start_new_thread(thread_client, (conn,))
