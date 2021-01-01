import pygame
from settings import *


class World:
    def __init__(self, map):
        self.map = list(map)
        self.objects = set()

        for i, row in enumerate(self.map):
            for j, obj_char in enumerate(row):
                if obj_char == 'W':
                    self.objects.add(
                        Wall(
                            TILE_SIZE * j,
                            TILE_SIZE * i
                        )
                    )
                elif obj_char == 'w':
                    self.objects.add(
                        TexturedWall(
                            TILE_SIZE * j,
                            TILE_SIZE * i,
                            'images/wall.jpg'
                        )
                    )
                elif obj_char == '.':
                    pass
                else:
                    assert ValueError(
                        f"Object '{obj_char}' is undefined"
                    )


class WorldObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.info = {
            'type': type(self).__name__,
            'x': self.x,
            'y': self.y
        }

    def get_info(self):
        return self.info


class Wall(WorldObject):
    def __init__(self, x, y):
        super().__init__(x, y)


class TexturedWall(Wall):
    def __init__(self, x, y, texture):
        super().__init__(x, y)
        self.texture = pygame.image.load(texture).convert()
        self.info['texture'] = self.texture
