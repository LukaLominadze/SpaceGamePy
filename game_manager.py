import random
from entities import *
from game_data import ENTITY_SIZE, ENEMY_IMG, ENEMY_SPEED


class GameManager:
    def __init__(self, enemy_spawn_time):
        self.possible_spawn_pos = (0, 360)
        self.spawn_pos = (511, random.randint(self.possible_spawn_pos[0], self.possible_spawn_pos[1]))
        self.spawn_time = enemy_spawn_time * 60  # Converting seconds to ticks

        self.time = pygame.time.get_ticks()
        self.elapsed_time = self.time

        self.enemies = []

    def update(self):
        current_time = pygame.time.get_ticks()
        time_since_last_spawn = current_time - self.time

        # Update existing entities
        try:
            for key, entity_data in Entity.entities.items():

                entity = entity_data['entity']

                entity.update()
                entity.add_update()

                if entity.pos[0] < -32:
                    entity.destroy()
        except RuntimeError:
            pass

        if time_since_last_spawn > self.spawn_time:

            Enemy(self.spawn_pos, ENEMY_IMG, ENTITY_SIZE, (1, 1), ENEMY_SPEED, 10)

            self.spawn_pos = (480, random.randint(self.possible_spawn_pos[0], self.possible_spawn_pos[1]))
            self.time = current_time

            self.elapsed_time = 0
