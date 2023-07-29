from typing import Tuple
import pygame
from pygame import Surface
import color

from network import Network
from env import *

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

    def network_friendly_stringify(self):
        return str(self.player_id) + ", " + self.color_str + ", " + str(self.x) + ", " + str(self.y)


    def connect(self):
        self.network = Network(HOST, PORT)
        info = self.network.connect()
        self.create_player_from_server_info(info)

    def create_player_from_server_info(self, info):
        info_tuple_str = tuple(map(str, info.split(', ')))
        self.player_id = int(info_tuple_str[0])
        self.color_str = info_tuple_str[1]
        self.color = color.str_to_color(self.color_str)
        self.x = int(info_tuple_str[2])
        self.y = int(info_tuple_str[3])

    def update_player_from_server_info(self, info):
        info_tuple_str = tuple(map(str, info.split(', ')))
        self.x = int(info_tuple_str[2])
        self.y = int(info_tuple_str[3])

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

    def send(self, msg):
        return self.network.send(msg)

    def inform_server(self):
        info=self.network_friendly_stringify()
        return self.send(f"MOVE, {info}")


if __name__ == "__main__":
    p = Player(50, 50)
    # p.connect()
