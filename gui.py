import pygame
from player import Player
import color
from pygame import Surface

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
    p = Player()
    p.connect()
    win.fill(color.WHITE)
    p.draw(win)
    pygame.display.update()

    clock = pygame.time.Clock()
    opponent = None
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        p.move()
        if opponent is None:
            opponent_info = p.ask_for_opponent()
            if opponent_info:
                opponent = Player()
                opponent.create_player_from_server_info(opponent_info)
        if opponent:
            opponent_current_pickle = p.inform_server()
            opponent.update_from_pickle(opponent_current_pickle)
        redraw_window(win, p, opponent)


if __name__ == "__main__":
    main()
