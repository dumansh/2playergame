import pickle
import pygame
from player import Player
import color
from pygame import Surface
from network import Network

width = 500
height = 500

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Game")

clientNumber = 0


def redraw_window(win: Surface, player: Player, opponent: Player = None):
    win.fill(color.WHITE)

    if opponent:
        opponent.draw(win)
    player.draw(win)
    pygame.display.update()


def main():
    run = True
    server = Network()
    me: Player = server.connect()
    win.fill(color.WHITE)
    me.draw(win)
    pygame.display.update()

    clock = pygame.time.Clock()
    opponent = None
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        me.move()

        if opponent is None:
            opponent = server.ask_for_opponent()
        if opponent:
            # send my updated position to server and get opponent's updated position from server
            opponent = server.update(me)

        redraw_window(win, me, opponent)


if __name__ == "__main__":
    main()
