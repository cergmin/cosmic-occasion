from math import sin, cos, radians
from settings import *
from ray import ray_cast


class Player:
    def __init__(self, x, y, vx=0, speed=100, health=100):
        self.x = x
        self.y = y
        self.vx = vx
        self.speed = speed
        self.health = health
        self.max_health = health

    def hit(self, health):
        '''Ударить игрока и снять определённое количество единиц здоровья'''

        self.health -= health
        self.health = max(0, self.health)

    def move(self, world, angle, distance, stop_distance=10):
        '''Передвижение игрока на distance в сторону angle,
           относительно взгяла игрока, если это возможно.'''

        angle += self.vx
        angle %= 360

        # Определяем количество свободного места вдоль оси y
        ray_distance_y = ray_cast(
            world,
            self.x,
            self.y,
            (90 if 0 <= angle <= 180 else -90),
            max_depth=(distance + 1)
        )[0]

        # Определяем количество свободного места вдоль оси x
        ray_distance_x = ray_cast(
            world,
            self.x,
            self.y,
            (180 if 90 <= angle <= 270 else 0),
            max_depth=(distance + 1)
        )[0]

        if ray_distance_x > (stop_distance + distance):
            # Если места по оси x достаточно,
            # чтобы пройти расстояние distance,
            # то двигаемся.
            self.x += distance * cos(radians(angle))
        else:
            # Если нет, то двигаемся на столько, на сколько можем
            self.x += (ray_distance_x - stop_distance) * cos(radians(angle))

        if ray_distance_y > (stop_distance + distance):
            # Если места по оси y достаточно,
            # чтобы пройти расстояние distance,
            # то двигаемся.
            self.y += distance * sin(radians(angle))
        else:
            # Если нет, то двигаемся на столько, на сколько можем
            self.y += (ray_distance_y - stop_distance) * sin(radians(angle))
