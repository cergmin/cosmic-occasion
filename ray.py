import pygame
from math import sin, cos, radians
from settings import *


class Ray:
    def __init__(self, world, screen, player):
        self.world = world
        self.screen = screen
        self.player = player

    def cast(self, x, y, vx, vy):
        for ray_length in range(0, MAX_DEPTH, RAY_STEP):
            ray_x = self.player.x + cos(radians(vx)) * ray_length
            ray_y = self.player.y + sin(radians(vx)) * ray_length
            # pygame.draw.line(
            #     self.screen,
            #     (255, 0, 0),
            #     (
            #         self.player.x,
            #         self.player.y
            #     ),
            #     (
            #         ray_x,
            #         ray_y
            #     ),
            #     2
            # )

            ray_collided = False
            for obj in self.world.objects:
                if (ray_x // TILE_SIZE, ray_y // TILE_SIZE) == \
                   (obj.x // TILE_SIZE, obj.y // TILE_SIZE):
                    ray_collided = True

            if ray_collided:
                return ray_length

        return MAX_DEPTH