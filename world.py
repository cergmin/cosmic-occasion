from math import *
from pygame.mixer import Sound
from pygame import sprite, transform
from settings import *


class World:
    def __init__(self, map):
        self.map = list(map)
        self.objects = dict()
        self.sprite_group = sprite.Group()

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
    
    def add_sprite(self, sprite):
        self.sprite_group.add(sprite)
    
    def update_sprites(self, player):
        self.sprite_group.update(player)


class WorldSprite(sprite.Sprite):
    def __init__(self, sprite_x, sprite_y, sprite_height, image, rc):
        super().__init__()
        self.rc = rc
        self.image = rc.get(image)
        self.rect = self.image.get_rect()
        
        self.sprite_image = image
        self.sprite_x = sprite_x
        self.sprite_y = sprite_y
        self.sprite_h = sprite_height
        self.sprite_scale_k = self.rect.size[0] / self.rect.size[1]

        self.rect.x = 0
        self.rect.y = (HEIGHT - self.rect.size[1]) / 2
        
        self.set_scale(1)
    
    def draw(self, screen):
        # Собственная функция рисования,
        # чтобы можно было рисовать спрайты по отдельности
        screen.blit(self.image, self.rect)
    
    def set_scale(self, scale):
        self.rect.size = (
            scale * self.sprite_h,
            scale * self.sprite_h * self.sprite_scale_k
        )

        self.image = transform.scale(
            self.rc.get(self.sprite_image),
            self.rect.size
        )

        self.rect.y = (HEIGHT - self.rect.size[1]) / 2
    
    def update_perspective(self, player):
        # Изменение пололжения спрайта относительно поворота игрока
        sprite_angle = degrees(
            atan2(
                player.y - self.sprite_y,
                player.x - self.sprite_x
            )
        )

        delta_angle = (sprite_angle - player.vx) % 360
        delta_angle = 180 - delta_angle

        self.rect.x = (
            (FOV / 2 - delta_angle) / FOV * WIDTH
        )

        # Изменение размера спрайта относительно положения игрока
        sprite_distance = (
            (self.sprite_x - player.x) ** 2 +
            (self.sprite_y - player.y) ** 2
        ) ** 0.5

        self.set_scale(DIST / max(sprite_distance, 0.1))

    def update(self, player):
        self.update_perspective(player)


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

        self.sound = shot_sound

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