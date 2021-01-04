from math import sin, cos, radians
import pygame
from settings import *
from utilities import *

def ray_cast(world, x, y, cur_angle, max_depth=None):
    if max_depth is None:
        max_depth = MAX_DEPTH

    xm, ym = mapping(x, y)
    cur_angle_sin = sin(radians(cur_angle))
    cur_angle_cos = cos(radians(cur_angle))
    # Защищает от деления на ноль,
    # когда у нас идёт деление на sin или cos
    cur_angle_sin = (cur_angle_sin if cur_angle_sin else 0.00001)
    cur_angle_cos = (cur_angle_cos if cur_angle_cos else 0.00001)
    
    # Пересечения с горизонталями
    obj_info_x = {'id': -1, 'type': 'none'}
    offset_x = 0
    if cur_angle_sin >= 0:
        ray_y = ym + GRID_SIZE
        dy = 1  # Направление движения луча: вдоль оси y
    else:
        ray_y = ym
        dy = -1  # Направление движения луча: против оси y
    for i in range(0, MAX_DEPTH, GRID_SIZE):            
        depth_x = (ray_y - y) / cur_angle_sin
        ray_x = x + depth_x * cur_angle_cos
        offset_x = x + depth_x * cur_angle_cos
        if mapping(ray_x, ray_y + dy) in world.objects:
            obj_info_x = world.objects[
                mapping(ray_x, ray_y + dy)
            ].get_info()
            break
        
        ray_y += dy * GRID_SIZE
    
    # Пересечения с вертикалями
    obj_info_y = {'id': -1, 'type': 'none'}
    offset_y = 0
    if cur_angle_cos >= 0:
        ray_x = xm + GRID_SIZE
        dx = 1  # Направление движения луча: вдоль оси x
    else:
        ray_x = xm
        dx = -1  # Направление движения луча: против оси x
    for i in range(0, MAX_DEPTH, GRID_SIZE):
        depth_y = (ray_x - x) / cur_angle_cos
        ray_y = y + depth_y * cur_angle_sin
        offset_y = y + depth_y * cur_angle_sin
        if mapping(ray_x + dx, ray_y) in world.objects:
            obj_info_y = world.objects[
                mapping(ray_x + dx, ray_y)
            ].get_info()
            break
        
        ray_x += dx * GRID_SIZE
    # Определение ближайшего пересечения
    if depth_x < depth_y:
        depth = depth_x
        offset = offset_x
        obj_info = obj_info_x
    else:
        depth = depth_y
        offset = offset_y
        obj_info = obj_info_y
    return (
        depth,
        offset % GRID_SIZE,
        obj_info
    )