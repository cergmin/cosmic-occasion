import pygame
from math import sin, cos, radians
from settings import *
from utilities import *


class Ray:
    def __init__(self, world, player):
        self.world = world
        self.player = player
    
    # cast с оптимизацией
    def cast(self, x, y, vx, vy):
        xm, ym = mapping(x, y)
        cur_angle = vx - FOV / 2

        cur_angle_sin = sin(radians(cur_angle))
        cur_angle_cos = cos(radians(cur_angle))

        # Защищает от деления на ноль,
        # когда у нас идёт деление на sin или cos
        cur_angle_sin = (cur_angle_sin if cur_angle_sin else 0.00001)
        cur_angle_cos = (cur_angle_cos if cur_angle_cos else 0.00001)

        for n in range(RAYS_AMOUNT):
            # Пересечения с вертикалями
            obj_info_x = {'type': 'none'}
            offset_y = 0
            if cur_angle_cos >= 0:
                ray_x = xm + TILE_SIZE
                dx = 1
            else:
                ray_x = xm
                dx = -1

            for i in range(0, WIDTH, TILE_SIZE):
                depth_x = (ray_x - x) / cur_angle_cos
                ray_y = y + depth_x * cur_angle_sin
                offset_y = y + depth_x * cur_angle_sin

                ray_collided = False
                for obj in self.world.objects:
                    if mapping(ray_x + dx, ray_y) == \
                       mapping(obj.x, obj.y):
                        obj_info_x = obj.get_info()
                        ray_collided = True
                
                if ray_collided:
                    break
                ray_x += dx * TILE_SIZE
            
            # Пересечения с горизонталями
            obj_info_y = {'type': 'none'}
            offset_x = 0
            if cur_angle_sin >= 0:
                ray_y = ym + TILE_SIZE
                dy = 1
            else:
                ray_y = ym
                dy = -1

            for i in range(0, HEIGHT, TILE_SIZE):
                depth_y = (ray_y - y) / cur_angle_sin
                ray_x = x + depth_y * cur_angle_cos
                offset_x = x + depth_y * cur_angle_cos

                ray_collided = False
                for obj in self.world.objects:
                    if mapping(ray_x, ray_y + dy) == \
                       mapping(obj.x, obj.y):
                        obj_info_y = obj.get_info()
                        ray_collided = True
                
                if ray_collided:
                    break
                ray_y += dy * TILE_SIZE

            if depth_x < depth_y:
                depth = depth_x
                offset = offset_y
                obj_info = obj_info_x
            else:
                depth = depth_y
                offset = offset_x
                obj_info = obj_info_y

            # print(offset_x % TILE_SIZE, offset_y % TILE_SIZE)

            return (
                depth,
                offset,
                obj_info
            )