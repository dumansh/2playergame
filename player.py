from __future__ import annotations
from typing import Tuple
import pygame
import pickle
from pygame import Surface
import color

STEP_SIZE = 3


class Player():
    def __init__(self, player_id=None,
                 width: int = 20,
                 height: int = 20,
                 x: int = 0, y: int = 0,
                 color_tuple: Tuple[int, int, int] = None,
                 color_str: str = None,
                 joined: bool = False
                 ):

        self.player_id = player_id
        self.info = None
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color_tuple
        self.step = STEP_SIZE
        self.color_str = color_str
        self.joined = joined

        if color_str and not color_tuple:
            self.color = color.str_to_color(color_str)

    def pickle(self):
        return pickle.dumps(self)

    @property
    def rect(self):
        return self.x, self.y, self.width, self.height

    def __repr__(self):
        return str(self.player_id) + ": " + self.color_str + " (" + str(self.x) + ", " + str(self.y) + ")"

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

    def opponent_id(self):
        if self.player_id is not None:
            return 3 - self.player_id

    def update(self, p: Player):
        self.x = p.x
        self.y = p.y


