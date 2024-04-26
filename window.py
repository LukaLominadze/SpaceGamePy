import pygame
from entities import Entity
from game_data import BG


class Window:
    def __init__(self, title, win_res, game_res, fps=60):
        pygame.init()

        self.screen = pygame.display.set_mode(win_res)

        if game_res is not None:
            self.display = pygame.Surface(game_res)
        else:
            self.display = pygame.Surface(win_res)

        pygame.display.set_caption(title)

        self.clock = pygame.time.Clock()
        self.clock.tick(fps)

    def clear(self, color=BG):
        self.display.fill(color)

    def render(self, surface, pos):
        self.display.blit(surface, pos)

    def render_objs(self):

        try:
            for key, entity in Entity.entities.items():
                self.display.blit(entity['entity'].img, entity['pos'])
                # pygame.draw.rect(self.display, (0, 75, 50, 100), entity['rect'])
        except RuntimeError:
            pass

    def render_display(self):
        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

    def update(self):
        pygame.display.update()
