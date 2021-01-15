from math import *
from pygame.mixer import Sound
from pygame import sprite, transform
from ray import ray_cast
from utilities import *
from settings import *


class World:
    def __init__(self, map):
        self.map = list(map)
        self.objects = dict()
        self.sprite_group = sprite.Group()
        self.route_hash = dict()

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
    
    def update_sprites(self, player, tick, *args, **kwargs):
        self.sprite_group.update(self, player, tick, *args, **kwargs)

    def get_route(self, x1, y1, x2, y2, visited_cells=None):
        x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))

        if visited_cells is None:
            visited_cells = dict()

        visited_cells[x1, y1] = True

        if (x1, y1) == (x2, y2):
            return [(x1, y1)]

        if (x1, y1, x2, y2) in self.route_hash:
            return self.route_hash[x1, y1, x2, y2]

        best_route = []
        for i, j in [
            (x1 + 1, y1),
            (x1, y1 + 1),
            (x1 - 1, y1),
            (x1, y1 - 1)
        ]:
            if (i, j) in visited_cells and visited_cells[i, j]:
                continue

            if (GRID_SIZE * i, GRID_SIZE * j) in self.objects or not \
               (0 <= j < len(self.map) and 0 <= i < len(self.map[j])):
                continue
            
            route = self.get_route(i, j, x2, y2, visited_cells)
            visited_cells[i, j] = False

            if len(route) > 0 and (
                len(best_route) == 0 or
                len(best_route) > len(route) + 1
            ):
                best_route = [(x1, y1)] + route

        self.route_hash[x1, y1, x2, y2] = best_route
        return best_route

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

        if WIDTH > self.rect.x > -self.rect.size[0]:
            screen.blit(self.image, self.rect)
    
    def get_distance(self, player):
        # Получение расстояние до игрока
        return (
            (self.sprite_x - player.x) ** 2 +
            (self.sprite_y - player.y) ** 2
        ) ** 0.5
    
    def set_scale(self, scale):
        self.rect.size = (
            min(scale * self.sprite_h, HEIGHT * 2),
            min(scale * self.sprite_h, HEIGHT * 2) * self.sprite_scale_k
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
        self.set_scale(DIST / max(self.get_distance(player), 0.5))

    def update(self, world, player, tick, *args, **kwargs):
        self.update_perspective(player)


class Enemy(WorldSprite):
    def __init__(self, sprite_x, sprite_y, sprite_height, image, rc,
                 health=100, damage=10, speed=100, visual_range=200):
        super().__init__(sprite_x, sprite_y, sprite_height, image, rc)
        
        self.health = max(0, health)
        self.damage = damage
        self.speed = speed
        self.visual_range = visual_range
    
    def check_direct_visibility(self, world, player):
        distance_to_player = self.get_distance(player)

        angle_to_player = degrees(
            atan2(
                player.y - self.sprite_y,
                player.x - self.sprite_x
            )
        )

        distance_to_first_object = ray_cast(
            world,
            self.sprite_x,
            self.sprite_y,
            angle_to_player,
            max_depth=(distance_to_player + 5)
        )[0]

        return distance_to_first_object >= distance_to_player


    def get_shot(self, player):
        # Определение того, насколько точно попали во врага
        # и убавление уровня здоровья
        sprite_angle = degrees(
            atan2(
                player.y - self.sprite_y,
                player.x - self.sprite_x
            )
        )

        delta_angle = (sprite_angle - player.vx) % 360
        delta_angle = 180 - delta_angle

        # delta_pixel = (FOV / 2 - delta_angle) / FOV * WIDTH

        if delta_angle <= 5:
            self.health -= 100
        
        # if abs(
        #     self.rc.get(self.sprite_image).get_rect().size[0] / 2 -
        #     delta_pixel
        # ) <= self.rc.get(self.sprite_image).get_rect().size[0] / 2:
        #     self.health -= 100

    def atack(self, player):
        pass
    
    # Честное построение маршрута от врага до игрока
    # с обхождением препятствий. Метод основан на dfs,
    # клетка карты представляется в виле вершины графа,
    # у которой может быть от 1 до 4 рёбер.
    def move_dfs(self, world, tick, x, y):
        route = world.get_route(
            int(self.sprite_x // GRID_SIZE),
            int(self.sprite_y // GRID_SIZE),
            int(x // GRID_SIZE),
            int(y // GRID_SIZE)
        )

        if len(route) < 2:
            return False

        next_position = (
            route[1][0] * GRID_SIZE + GRID_SIZE / 2,
            route[1][1] * GRID_SIZE + GRID_SIZE / 2,
        )
        
        # Метод прямого перемещения используется,
        # чтобы присутствовала коллизия с объектами
        self.move_direct(world, tick, *next_position)

    # Движение к игроку напрямую с учётом коллизий.
    # Не обхожит препятсвия, но зато работает бысрее,
    # чем Enemy.move_dfs(...)
    def move_direct(self, world, tick, x, y, stop_distance=40):
        distance = self.speed * tick

        move_direction = atan2(
            y - self.sprite_y,
            x - self.sprite_x
        )

        ray_distance_y = ray_cast(
            world,
            self.sprite_x,
            self.sprite_y,
            (90 if 0 <= degrees(move_direction) <= 180 else -90),
            max_depth=(distance + 1)
        )[0]

        ray_distance_x = ray_cast(
            world,
            self.sprite_x,
            self.sprite_y,
            (180 if 90 <= degrees(move_direction) <= 270 else 0),
            max_depth=(distance + 1)
        )[0]
        
        if ray_distance_x > (stop_distance + distance):
            self.sprite_x += distance * cos(move_direction)
        else:
            self.sprite_x += (ray_distance_x - stop_distance) * \
                             cos(move_direction)
        
        if ray_distance_y > (stop_distance + distance):
            self.sprite_y += distance * sin(move_direction)
        else:
            self.sprite_y += (ray_distance_y - stop_distance) * \
                             sin(move_direction)

    def update(self, world, player, tick, *args, **kwargs):
        self.update_perspective(player)

        if 'shot' in kwargs and kwargs['shot']:
            self.get_shot(player)

            if self.health <= 0:
                world.sprite_group.remove(self)

        if self.get_distance(player) <= self.visual_range:
            if self.check_direct_visibility(world, player):
                self.move_direct(world, tick, player.x, player.y)
            else:
                self.move_dfs(world, tick, player.x, player.y)


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