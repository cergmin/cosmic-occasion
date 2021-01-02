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
                            'wall'
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
    def __init__(self, x, y, texture_name):
        super().__init__(x, y)
        self.texture_name = texture_name
        self.info['texture_name'] = self.texture_name


class Weapon:
    def __init__(self, normal, aimed_normal, shot_animation, aiming_animation,
                 aimed_shot_animation, shot_sound, duration=0.5):
        # self.animations = {
        #   'название_анимации': [
        #       массив_кадров_анимации,
        #       длительность_показа_1_кадра
        #   ]
        # }
        # 
        # Кадры представленны в виде массива названий картинок,
        # которые хранятся в ImageController.
        # Длительность показа измеряется в секундах.
        self.animations = {
            'normal': [normal, 0],
            'aimed_normal': [aimed_normal, 0],
            'shot': [
                shot_animation,
                duration / len(shot_animation)],
            'aiming': [
                aiming_animation,
                duration / len(aiming_animation)],
            'aimed_shot': [
                aimed_shot_animation,
                duration / len(aimed_shot_animation)]
        }

        self.sound = pygame.mixer.Sound(shot_sound)

        self.timer = 0
        self.state = ['normal', 0]

    def set_state(self, state):
        if state in self.animations:
            self.state = [state, 0]

    def update(self, tick):
        self.timer += tick

        if self.state[0] == 'normal':
            self.timer = 0
            self.state[1] = 0
        elif self.state[0] == 'shot':
            while self.timer > self.animations['shot'][1]:
                if self.state[1] + 1 >= len(self.animations['shot'][0]):
                    self.state[0] = 'normal'
                    self.state[1] = 0
                    self.timer = 0
                    break
                else:
                    self.state[1] += 1
                self.timer -= self.animations['shot'][1]
        elif self.state[0] == 'aiming':
            while self.timer > self.animations['aiming'][1]:
                if self.state[1] + 1 >= len(self.animations['aiming'][0]):
                    self.state[0] = 'aimed_normal'
                    self.state[1] = 0
                    self.timer = 0
                    break
                else:
                    self.state[1] += 1
                self.timer -= self.animations['aiming'][1]