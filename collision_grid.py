import pygame
from game_data import GAME_RES, TILE_SIZE
from mathf import clamp


class CollisionGrid:
    grid = {}

    def __init__(self, game_res, tile_size=(32, 32)):
        self.game_res = game_res
        self.tile_size = tile_size

        self.row = game_res[0] // tile_size[0]
        self.column = game_res[1] // tile_size[1]

        for col in range(self.column):
            for row in range(self.row):
                CollisionGrid.grid[f'{row};{col}'] = []

    @staticmethod
    def get(row, col):
        return CollisionGrid.grid[f'{row};{col}']

    @staticmethod
    def add(row, col, collider):
        CollisionGrid.grid[f'{row};{col}'].append(collider)

    @staticmethod
    def remove(row, col, collider):
        CollisionGrid.grid[f'{row};{col}'].remove(collider)


class Collider(pygame.Rect):
    def __init__(self, left, top, width, height, parent):
        super().__init__(left, top, width, height)
        self.parent = parent

        self.pos = [left, top]

        self.row = int(self.pos[0] / 32)  # Tile size
        self.col = int(self.pos[1] / 32)

        try:
            CollisionGrid.add(self.row, self.col, self)
        except KeyError or ValueError as e:
            print(f'{self} -> {e}')

        self.last_grid = CollisionGrid.get(self.row, self.col)

    def update(self, pos):
        self.pos = pos
        self.left = self.pos[0]
        self.top = self.pos[1]

        self.row = clamp(self.pos[0] // 32, 0, 15)  # Tile size
        self.col = clamp(self.pos[1] // 32, 0, 11)

        if self.last_grid != CollisionGrid.get(self.row, self.col):
            try:
                self.last_grid.remove(self)
                CollisionGrid.add(self.row, self.col, self)
                self.last_grid = CollisionGrid.get(self.row, self.col)
            except KeyError or ValueError as e:
                print(f'{self} -> {e}')

    def check_collision(self):
        for col in range(self.col - 1, self.col + 2):
            if col < 0 or col > GAME_RES[1] // TILE_SIZE[1] - 1:
                continue
            for row in range(self.row - 1, self.row + 2):
                if row < 0 or row > GAME_RES[0] // TILE_SIZE[0] - 1:
                    continue
                grid_colliders = CollisionGrid.get(row, col)
                for collider in grid_colliders:
                    if collider != self:
                        if self.parent.target_tag is None:
                            if self.colliderect(collider):
                                return True
                        elif self.parent.target_tag == collider.parent.tag:
                            if self.colliderect(collider):
                                return True
        return False

    def destroy(self):
        self.last_grid.remove(self)
