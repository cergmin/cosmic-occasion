import pygame
from math import sin, cos, radians
from settings import *


class Ray:
    def __init__(self, world, player):
        self.world = world
        self.player = player

    def cast(self, x, y, vx, vy):
        for ray_length in range(0, MAX_DEPTH, RAY_STEP):
            ray_x = self.player.x + cos(radians(vx)) * ray_length
            ray_y = self.player.y + sin(radians(vx)) * ray_length

            for obj in self.world.objects:
                if (ray_x // TILE_SIZE, ray_y // TILE_SIZE) == \
                   (obj.x // TILE_SIZE, obj.y // TILE_SIZE):
                    return (
                        ray_length,
                        obj.get_info()
                    )

        return (
            MAX_DEPTH,
            {
                'type': 'None'
            }
        )