import sys
from window import Window
from game_manager import *
from game_data import PLAYER_START_POS, PLAYER_IMG, ENTITY_SIZE, PLAYER_SPEED
from collision_grid import CollisionGrid
from audio_manager import AudioManager


class Application:
    def __init__(self, title, win_res, game_res=None):
        self.window = Window(title, win_res, game_res)
        self.collision_grid = CollisionGrid(game_res, ENTITY_SIZE)
        self.game_manager = GameManager(12)
        AudioManager.init()
        self.player = Player(PLAYER_START_POS, PLAYER_IMG, ENTITY_SIZE, (.8, .8), PLAYER_SPEED)

    def run(self):
        AudioManager.loop_music('assets/OST_1.wav')
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Application.quit()

                self.player.handle_input(event)

            self.player.move()

            self.game_manager.update()

            if not self.player.is_alive:
                Application.quit()

            self.window.clear()
            self.window.render_objs()
            self.window.render_display()
            self.window.update()

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()