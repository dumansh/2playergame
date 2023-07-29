import pygame
from player import Player
import color
from pygame import Surface
import time

width = 500
height = 500

win = pygame.display.set_mode((width, height))

pygame.display.set_caption("My Game")

clientNumber = 0


def redraw_window(win: Surface, player: Player, opponent: Player):
    win.fill(color.WHITE)
    player.draw(win)
    opponent.draw(win)
    pygame.display.update()


def main():
    run = True
    p = Player()
    p.connect()

    opponent_data = p.send("OPPONENT")
    opponent = None

    clock = pygame.time.Clock()
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        p.move()
        if opponent_data == "NO_OPPONENT":
            win.fill(color.WHITE)
            p.draw(win)
            pygame.display.update()
        while opponent_data == "NO_OPPONENT":
            opponent_data = p.send("OPPONENT")

        if opponent is None:
            opponent = Player()
            opponent.create_player_from_server_info(opponent_data)

        opponent_current_data = p.inform_server()
        opponent.update_player_from_server_info(opponent_current_data)
        redraw_window(win, p, opponent)


main()
