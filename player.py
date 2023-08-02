from typing import Tuple
import pygame
import pickle
from pygame import Surface
import color

from network import Network
from playerdata import PlayerData
from env import *
from helpers import META_WIDTH
from helpers import make_packet, META_WIDTH

STEP_SIZE = 3


class Player():
    def __init__(self, player_id=None, width: int = 20, height: int = 20, x=0, y=0, color_tuple=None, color_str=None):
        self.player_id = player_id
        self.info = None
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color_tuple
        self.step = STEP_SIZE
        self.color_str = color_str

        if color_str and not color_tuple:
            self.color = color.str_to_color(color_str)

    @property
    def rect(self):
        return (self.x, self.y, self.width, self.height)

    def __repr__(self):
        return str(self.player_id) + ": " + self.color_str + " (" + str(self.x) + ", " + str(self.y) + ")"
    @property
    def playerinfo(self):
        return PlayerData(self.player_id, self.color_str, self.x, self.y, True)


    def connect(self):
        self.network = Network(HOST, PORT)
        playerinfo = self.network.connect()
        self.create_player_from_server_info(playerinfo)

    def create_player_from_server_info(self, playerinfo: PlayerData):

        self.player_id = playerinfo.player_id
        self.color_str = playerinfo.color_str
        self.color = color.str_to_color(self.color_str)
        self.x = playerinfo.posX
        self.y = playerinfo.posY

    def update_from_pickle(self, data: bytes):
        playerinfo = pickle.loads(data)
        self.x = playerinfo.posX
        self.y = playerinfo.posY

    def draw(self, win: Surface):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.step

        if keys[pygame.K_RIGHT]:
            self.x += self.step

        if keys[pygame.K_UP]:
            self.y -= self.step

        if keys[pygame.K_DOWN]:
            self.y += self.step

        # print(self.rect)

    def send(self, msg: bytes):
        return self.network.send(msg)

    def sendstr(self, msg: str):
        return self.network.send(msg.encode())

    def ask_for_opponent(self):
        opponent_info = self.sendstr("OPPONENT")
        meta=opponent_info[:META_WIDTH].decode()
        if "NO_OPPONENT" not in meta:
            opponent = pickle.loads(opponent_info[META_WIDTH:])
            return opponent



    def inform_server(self):
        packet=make_packet("MOVE", self.playerinfo.pickle())
        return self.send(packet)


if __name__ == "__main__":
    p = Player()
    p.connect()
