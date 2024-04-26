import pygame as pg
import sys


def clamp(value, minimum, maximum):
    if value < minimum:
        return minimum
    elif value > maximum:
        return maximum
    else:
        return value


pg.init()

window = pg.display
game_screen = pg.Surface((256, 256))
screen = window.set_mode((600, 600))

window.set_caption("MyGame")

player_pos = [100, 200]
player = pg.Rect(player_pos[0], player_pos[1], 64, 32)

ball = pg.Rect(100, 20, 16, 16)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                pass

    player.top = player_pos[1]

    game_screen.fill((50, 200, 100))

    screen.blit(pg.transform.scale(game_screen, screen.get_size()), (0, 0))
    window.update()
