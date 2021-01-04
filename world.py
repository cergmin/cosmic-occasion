from pygame.mixer import Sound
from settings import *


class World:
    def __init__(self, map):
        self.map = list(map)
        self.objects = dict()

        for i, row in enumerate(self.map):
            for j, obj_char in enumerate(row):
                if obj_char == 'W':
                    self.objects[(
                        GRID_SIZE * j,
                        GRID_SIZE * i
                    )] = Wall(
                        GRID_SIZE * j,
                        GRID_SIZE * i
                    )
                elif obj_char == 'w':
                    self.objects[(
                        GRID_SIZE * j,
                        GRID_SIZE * i
                    )] = TexturedWall(
                        GRID_SIZE * j,
                        GRID_SIZE * i,
                        'wall'
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
                 aimed_shot_animation, shot_sound, shot_duration=0.5,
                 aiming_duration=0.3):
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
                shot_duration / len(shot_animation)],
            'aiming': [
                aiming_animation,
                aiming_duration / len(aiming_animation)],
            'reversed_aiming': [
                aiming_animation[::-1],
                aiming_duration / len(aiming_animation)],
            'aimed_shot': [
                aimed_shot_animation,
                shot_duration / len(aimed_shot_animation)]
        }

        self.sound = Sound(shot_sound)

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
        if self.state[0] == 'aimed_normal':
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
        elif self.state[0] == 'aimed_shot':
            while self.timer > self.animations['aimed_shot'][1]:
                if self.state[1] + 1 >= len(self.animations['aimed_shot'][0]):
                    self.state[0] = 'aimed_normal'
                    self.state[1] = 0
                    self.timer = 0
                    break
                else:
                    self.state[1] += 1
                self.timer -= self.animations['aimed_shot'][1]
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
        elif self.state[0] == 'reversed_aiming':
            while self.timer > self.animations['reversed_aiming'][1]:
                if self.state[1] + 1 >= \
                   len(self.animations['reversed_aiming'][0]):
                    self.state[0] = 'normal'
                    self.state[1] = 0
                    self.timer = 0
                    break
                else:
                    self.state[1] += 1
                self.timer -= self.animations['reversed_aiming'][1]