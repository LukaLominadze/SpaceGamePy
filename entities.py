import pygame
from game_data import RED_BULLET_IMG, YELLOW_BULLET_IMG, BULLET_SPEED, GAME_RES, ENTITY_SIZE
from collision_grid import Collider
from mathf import clamp
from audio_manager import AudioManager


class Entity:
    entities = {}
    entity_count = 0

    def __init__(self, pos, img_src, size, coll_size=(1, 1), tag=None, target_tag=None):
        self.pos = list(pos)
        self.img_src = img_src
        self.size = size
        self.coll_size = coll_size
        self.tag = tag
        self.target_tag = target_tag

        self.img = pygame.transform.scale(pygame.image.load(img_src), self.size)

        self.collider = Collider(self.pos[0] + (self.size[0] / 2) * (1 - self.coll_size[0]),
                                 self.pos[1] + (self.size[1] / 2) * (1 - self.coll_size[1]),
                                 self.size[0] * self.coll_size[0],
                                 self.size[1] * self.coll_size[1],
                                 self)

        self.index = Entity.entity_count

        Entity.entities[self.index] = {'entity': self, 'pos': self.pos, 'rect': self.collider}
        Entity.entity_count += 1

    def update(self):

        self.collider.update([int(self.pos[0] + (self.size[0] / 2) * (1 - self.coll_size[0])),
                              int(self.pos[1] + (self.size[1] / 2) * (1 - self.coll_size[1]))])

        Entity.entities[self.index]['rect'] = self.collider

    def add_update(self):
        pass

    def move(self, speed):
        self.pos[0] += speed[0]
        self.pos[1] += speed[1]
        Entity.entities[self.index]['pos'] = self.pos

    def get_absolute_position(self):
        return self.pos[0] + self.size[0] / 2, self.pos[1] + self.size[1] / 2

    def destroy(self):
        Entity.entities.pop(self.index)
        self.collider.destroy()
        del self


class Player(Entity):
    def __init__(self, pos, img, size, coll_size=(1, 1), speed=0, tag='player', target_tag='enemy'):
        super().__init__(pos, img, size, coll_size, tag, target_tag)
        self.movement = [False, False, False, False, False]
        self.inputs = [pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a, pygame.K_SPACE]
        self.axis = [0, 0]
        self.speed = speed
        self.is_alive = True

    def handle_input(self, event):
        self.set_input(event, pygame.KEYDOWN, True)
        self.set_input(event, pygame.KEYUP, False)

        self.axis = [self.movement[2] - self.movement[3],
                     self.movement[1] - self.movement[0]]

        if self.movement[4]:
            self.shoot()
            self.movement[4] = False

    def add_update(self):
        if self.collider.check_collision():
            self.is_alive = False

    def set_input(self, event, e_type, value):
        if event.type == e_type:
            for i in range(len(self.inputs)):
                if event.key == self.inputs[i]:
                    self.movement[i] = value

    def move(self):
        self.pos[0] += self.axis[0] * self.speed
        self.pos[1] += self.axis[1] * self.speed

        self.pos[0] = clamp(self.pos[0], 0, GAME_RES[0] - ENTITY_SIZE[0])
        self.pos[1] = clamp(self.pos[1], 0, GAME_RES[1] - ENTITY_SIZE[1])

        Entity.entities[self.index]['pos'] = self.pos

    def shoot(self):
        Bullet(self.pos, YELLOW_BULLET_IMG, self.size, (0.7, 0.2), BULLET_SPEED, 'player_bullet', self.target_tag)
        AudioManager.play_audio('assets/Bullet.mp3', 0.15)


class Enemy(Entity):
    def __init__(self, pos, img, size, coll_size=(1, 1), speed=0, time_to_shoot=0, tag='enemy', target_tag='player_bullet'):
        super().__init__(pos, img, size, coll_size, tag, target_tag)
        self.speed = speed
        self.time_to_shoot = time_to_shoot * 60
        self.time = pygame.time.get_ticks()
        self.elapsed_time = self.time

    def add_update(self):
        self.move((-self.speed, 0))

        current_time = pygame.time.get_ticks()
        time_since_last_spawn = current_time - self.time

        if time_since_last_spawn > self.time_to_shoot:
            Bullet(self.pos, RED_BULLET_IMG, self.size, (0.7, 0.2), -BULLET_SPEED, self.tag, 'player')
            self.time = current_time
            self.elapsed_time = self.time

        if self.collider.check_collision():
            AudioManager.play_audio('assets/Damage.wav', 0.15)
            self.destroy()


class Bullet(Entity):
    def __init__(self, pos, img, size, coll_size=(1, 1), speed=0, tag=None, target_tag=None):
        super().__init__(pos, img, size, coll_size, tag, target_tag)
        self.speed = speed

    def add_update(self):
        self.move((self.speed, 0))

        if self.pos[0] > GAME_RES[0]:
            self.destroy()
