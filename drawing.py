from math import *
import pygame
from settings import *
from ray import ray_cast
from controllers import ResourceController


class ElementUI:
    def __init__(self, rc, x, y, width, height):
        self.rc = rc
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height,
        )

    def is_hover(self, cursor_x, cursor_y):

        return (self.x <= cursor_x <= self.x + self.width) and \
               (self.y <= cursor_y <= self.y + self.height)

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            (255, 0, 0),
            self.get_rect()
        )


class Text(ElementUI):
    def __init__(self, rc, x, y, width, height, text='',
                 text_color=(255, 255, 255), font=None,
                 align=None):
        super().__init__(rc, x, y, width, height)
        
        self.text = text
        self.text_color = text_color

        if font is None:
            # Шрифт по умолчанию
            self.font = pygame.font.SysFont('Arial', round(self.height * 0.5))
        else:
            self.font = font

        if str(align).lower() in ['left', 'start', 'begin']:
            self.align = 'left'
        elif str(align).lower() in ['center', 'centre', 'middle']:
            self.align = 'center'
        elif str(align).lower() in ['right', 'end']:
            self.align = 'right'
        else:
            # Выравнивание по умолчанию
            self.align = 'center'
    
    def set_text(self, text):
        self.text = text
    
    def draw(self, surface):
        text_surface = self.font.render(
            self.text,
            True,
            self.text_color
        )

        text_x = self.x
        text_y = self.y + (self.height - text_surface.get_size()[1]) // 2

        if self.align == 'center':
            text_x = self.x + (self.width - text_surface.get_size()[0]) // 2
        elif self.align == 'right':
            text_x = self.x + self.width - text_surface.get_size()[0]

        surface.blit(
            text_surface,
            (
                text_x,
                text_y
            )
        )


class Button(ElementUI):
    def __init__(self, rc, x, y, width, height,
                 img_start, img_between,
                 img_middle, img_end,
                 img_start_hover, img_between_hover,
                 img_middle_hover, img_end_hover,
                 img_start_clicked, img_between_clicked,
                 img_middle_clicked, img_end_clicked,
                 text='', text_color=(255, 255, 255),
                 text_color_hover=None,
                 text_color_clicked=None,
                 font=None):
        super().__init__(rc, x, y, width, height)

        self.text = text
        self.text_color = {
            'normal': text_color,
            'hover': text_color,
            'clicked': text_color
        }

        if text_color_hover is not None:
            self.text_color['hover'] = text_color_hover

        if text_color_clicked is not None:
            self.text_color['clicked'] = text_color_clicked

        if font is None:
            self.font = pygame.font.SysFont('Arial', round(self.height * 0.5))
        else:
            self.font = font

        self.img = {
            'normal_start': img_start,
            'normal_between': img_between,
            'normal_middle': img_middle,
            'normal_end': img_end,
            'hover_start': img_start_hover,
            'hover_between': img_between_hover,
            'hover_middle': img_middle_hover,
            'hover_end': img_end_hover,
            'clicked_start': img_start_clicked,
            'clicked_between': img_between_clicked,
            'clicked_middle': img_middle_clicked,
            'clicked_end': img_end_clicked
        }

        self.states_list = [
            'normal',
            'hover',
            'clicked-mousedown',
            'clicked-mouseup'
        ]
        self.state = self.states_list[0]
    
    def update_state(self, mouse):
        if self.is_hover(*mouse.get_pos()):
            if pygame.mouse.get_pressed(3)[0]:
                self.set_state('clicked-mousedown')
            elif self.state == 'clicked-mousedown':
                self.set_state('clicked-mouseup')
            else:
                self.set_state('hover')
        else:
            self.set_state('normal')

    def set_state(self, state):
        state = str(state).lower()
        if state not in self.states_list:
            self.state = self.states_list[0]
        else:
            self.state = state
    
    def get_state(self):
        return self.state

    def draw(self, surface):
        img_w = {}

        for i in filter(
            lambda x: x.startswith(self.state.split('-')[0] + '_'),
            self.img
        ):
            img_w[i.split('_')[-1]] = max(
                1,
                round(
                    self.rc.get(self.img[i]).get_size()[0] * \
                    (self.height / self.rc.get(self.img[i]).get_size()[1])
                )
            )

        img_amount = [
            ['start', min(img_w['start'], self.width // 2)],
            ['between', 0],
            ['middle', 0],
            ['between', 0],
            ['end', min(img_w['end'], self.width // 2)]
        ]

        img_amount[1][1] = self.width - \
                           (img_amount[0][1] + img_amount[4][1])

        if img_amount[1][1] >= img_w['middle']:
            img_amount[2][1] = img_w['middle']
            img_amount[1][1] -= img_w['middle']

        if img_amount[1][1] % 2:
            img_amount[3][1] = 1

        img_amount[1][1] = img_amount[1][1] // 2
        img_amount[3][1] = img_amount[1][1]

        x_offset = 0
        for i in img_amount:
            scaled_img = pygame.transform.scale(
                self.rc.get(self.img[self.state.split('-')[0] + '_' + i[0]]),
                (
                    i[1],
                    self.height
                )
            )

            surface.blit(
                scaled_img,
                (
                    self.x + x_offset,
                    self.y
                )
            )

            x_offset += i[1]

        text_surface = self.font.render(
            self.text,
            True,
            self.text_color[self.state.split('-')[0]]
        )
        surface.blit(
            text_surface,
            (
                self.x + (self.width - text_surface.get_size()[0]) // 2,
                self.y + (self.height - text_surface.get_size()[1]) // 2
            )
        )


class Slider(ElementUI):
    def __init__(self, rc, x, y, width, height,
                 img_start, img_start_between, img_end_between,
                 img_end, img_pointer, current_value=None, min_value=0,
                 max_value=100, value_step=1):
        super().__init__(rc, x, y, width, height)

        self.img = {
            'start': img_start,
            'start_between': img_start_between,
            'end_between': img_end_between,
            'end': img_end,
            'pointer': img_pointer
        }
        
        self.min_value = min(min_value, max_value)
        self.max_value = max(self.min_value, max_value)
        self.value_step = value_step
        self.value_step_offset = self.min_value % value_step

        if current_value is None:
            self.value = self.min_value
        else:
            self.value = max(
                min_value,
                min(
                    max_value,
                    current_value
                )
            )
        
        self.states_list = [
            'slider-mouseup',
            'slider-mousedown'
        ]
        self.state = self.states_list[0]
    
    def update_state(self, mouse):
        if not mouse.get_pressed(3)[0]:
            self.set_state('slider-mouseup')

        if self.get_state() == 'slider-mousedown' or \
           (self.is_hover(*mouse.get_pos()) and mouse.get_pressed(3)[0]):
            if mouse.get_pressed(3)[0]:
                self.set_state('slider-mousedown')

            self.set_percentage(
                (
                    mouse.get_pos()[0] - self.x
                ) / self.width,
                min_limit=True,
                max_limit=True,
                step_limit=True
            )

    def set_state(self, state):
        state = str(state).lower()
        if state not in self.states_list:
            self.state = self.states_list[0]
        else:
            self.state = state
    
    def get_state(self):
        return self.state

    def set_value(self, value, min_limit=False,
                  max_limit=False, step_limit=False):
        if step_limit and value % self.value_step != self.value_step_offset:
            value -= (value % self.value_step) - self.value_step_offset

        if min_limit and value < self.min_value:
            value = self.min_value
        
        if max_limit and value > self.max_value:
            value = self.max_value

        self.value = value
    
    def get_value(self):
        return self.value
    
    def set_percentage(self, percentage, min_limit=False,
                       max_limit=False, step_limit=False):
        value = (
            self.max_value - self.min_value
        ) * percentage + self.min_value

        self.set_value(value, min_limit, max_limit, step_limit)
    
    def get_percentage(self):
        return (
            self.value - self.min_value
        ) / (
            self.max_value - self.min_value
        )

    def draw(self, surface):
        img_w = {}

        for i in self.img:
            img_w[i] = max(
                1,
                round(
                    self.rc.get(self.img[i]).get_size()[0] * \
                    (self.height / self.rc.get(self.img[i]).get_size()[1])
                )
            )

        img_amount = [
            [
                'start',
                min(
                    img_w['start'],
                    self.width // 2
                )
            ],
            ['start_between', 0],
            ['end_between', 0],
            [
                'end',
                min(
                    img_w['start'],
                    self.width // 2
                )
            ]
        ]

        width_rest = self.width - (
            img_amount[0][1] + 
            img_amount[3][1]
        )

        img_amount[1][1] = round(width_rest * self.get_percentage())
        img_amount[2][1] = width_rest - img_amount[1][1]

        x_offset = 0
        for i in img_amount:
            scaled_img = pygame.transform.scale(
                self.rc.get(self.img[i[0]]),
                (
                    i[1],
                    self.height
                )
            )

            surface.blit(
                scaled_img,
                (
                    self.x + x_offset,
                    self.y
                )
            )

            x_offset += i[1]
        
        pointer_width = round(
            self.rc.get(self.img['pointer']).get_size()[0] * (
                self.height / self.rc.get(self.img['pointer']).get_size()[1]  
            )
        )
        x_pointer_pos = self.x + (
            self.width - pointer_width
        ) * self.get_percentage()
        scaled_img = pygame.transform.scale(
            self.rc.get(self.img['pointer']),
            (
                pointer_width,
                self.height
            )
        )
        surface.blit(
            scaled_img,
            (
                x_pointer_pos,
                self.y
            )
        )


class Bar(ElementUI):
    def __init__(self, rc, x, y, width, height,
                 img_full, img_empty, img_pointer,
                 current_value=None, min_value=0,
                 max_value=100):
        super().__init__(rc, x, y, width, height)

        self.img = {
            'full': img_full,
            'empty': img_empty,
            'pointer': img_pointer
        }
        
        self.min_value = min(min_value, max_value)
        self.max_value = max(self.min_value, max_value)

        if current_value is None:
            self.value = self.min_value
        else:
            self.value = max(
                min_value,
                min(
                    max_value,
                    current_value
                )
            )
        
        self.state = 'bar'

    def set_state(self, state):
        pass
    
    def get_state(self):
        return self.state

    def set_value(self, value, min_limit=False, max_limit=False):
        if min_limit and value < self.min_value:
            value = self.min_value
        
        if max_limit and value > self.max_value:
            value = self.max_value

        self.value = value
    
    def get_value(self):
        return self.value
    
    def set_percentage(self, percentage, min_limit=False, max_limit=False):
        value = (
            self.max_value - self.min_value
        ) * percentage + self.min_value

        self.set_value(value, min_limit, max_limit)
    
    def get_percentage(self):
        return (
            self.value - self.min_value
        ) / (
            self.max_value - self.min_value
        )

    def draw(self, surface):
        empty_bar = pygame.transform.scale(
            self.rc.get(self.img['empty']),
            (
                self.width,
                self.height
            )
        )
        surface.blit(
            empty_bar,
            (
                self.x,
                self.y
            )
        )

        full_bar = pygame.transform.scale(
            self.rc.get(self.img['full']),
            (
                self.width,
                self.height
            )
        )
        full_bar = full_bar.subsurface((
            0,
            0,
            self.width * self.get_percentage(),
            self.height
        ))
        surface.blit(
            full_bar,
            (
                self.x,
                self.y
            )
        )

        pointer = pygame.transform.scale(
            self.rc.get(self.img['pointer']),
            (
                int(
                    self.height *
                    self.rc.get(self.img['pointer']).get_rect().size[0] /
                    self.rc.get(self.img['pointer']).get_rect().size[1]
                ),
                self.height
            )
        )
        surface.blit(
            pointer,
            (
                self.x + self.width * self.get_percentage() - \
                    pointer.get_rect().size[0] / 1.75,
                self.y
            )
        )


class Drawing:
    def __init__(self, screen, rc):
        self.screen = screen
        self.rc = rc
    
    def fps(self, clock):
        fps_amount = str(int(clock.get_fps()))
        font = pygame.font.SysFont('Arial', 36, bold=True)
        text = font.render(fps_amount, False, (255, 0, 0))
        self.screen.blit(
            text,
            (
                WIDTH - text.get_size()[0] - 7,
                0
            )
        )
    
    def minimap(self, world, player):
        map_scale = 30 / GRID_SIZE
        map_offset = (
            -200 * map_scale,
            -200 * map_scale
        )
        sprites_offset = (
            0 * map_scale,
            -260 * map_scale
        )
        map_size = (200, 200)
        map_full_size = (
            len(world.map[0]) * GRID_SIZE * map_scale,
            len(world.map) * GRID_SIZE * map_scale
        )
        map_real_size = (
            len(world.map[0]) * GRID_SIZE,
            len(world.map) * GRID_SIZE
        )

        # Фон всей карты
        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            (
                0,
                HEIGHT - map_size[1],
                map_size[0],
                map_size[1]
            )
        )
 
        map_surface = pygame.transform.scale(
            world.map_surface,
            (
                int(map_full_size[0]),
                int(map_full_size[1])
            )
        )

        map_subsurface_size = [0, 0, 0, 0]

        map_subsurface_size[0] = (
            player.x / map_real_size[0] * map_full_size[0] + map_offset[0]
        )

        map_subsurface_size[1] = (
            player.y / map_real_size[1] * map_full_size[1] + map_offset[1]
        )

        map_subsurface_size[2] = min(
            map_size[0],
            map_full_size[0] - map_subsurface_size[0]
        )

        map_subsurface_size[3] = min(
            map_size[1],
            map_full_size[1] - map_subsurface_size[1]
        )

        map_surface = map_surface.subsurface((
            max(0, map_subsurface_size[0]),
            max(0, map_subsurface_size[1]),
            map_subsurface_size[2] - max(0, -map_subsurface_size[0]),
            map_subsurface_size[3]
        ))

        self.screen.blit(
            map_surface,
            (
                max(0, -map_subsurface_size[0]),
                HEIGHT - map_size[1] + max(0, -map_subsurface_size[1])
            )
        )

        # Маркеры врагов
        for enemy in world.sprite_group:
            enemy_x = enemy.sprite_x / map_real_size[0] * \
                      map_full_size[0] + sprites_offset[0]
            enemy_y = (map_real_size[1] - enemy.sprite_y) / \
                      map_real_size[1] * map_full_size[1] + sprites_offset[1]

            if enemy_x - map_subsurface_size[0] > map_size[0] or \
               HEIGHT - enemy_y - map_subsurface_size[1] < \
               HEIGHT - map_size[1]:
                continue

            for radius, color in [
                (10, (255, 255, 255)),
                (8, (245, 52, 50)),
                (3, (255, 255, 255))
            ]:
                pygame.draw.circle(
                    self.screen,
                    color,
                    (
                        min(
                            map_size[0],
                            enemy_x - map_subsurface_size[0]
                        ),
                        max(
                            HEIGHT - map_size[1],
                            HEIGHT - enemy_y - map_subsurface_size[1]
                        )
                    ),
                    radius
                )
        
        # Стерлка взгляда игрока для маркера
        arrow_points = []
        for radius, deg in [
            (10, player.vx - 45),
            (17, player.vx),
            (10, player.vx + 45)
        ]:
            arrow_points.append((
                map_size[0] / 2 + radius * cos(radians(deg)),
                HEIGHT - map_size[0] / 2  + radius * sin(radians(deg))
            ))

        pygame.draw.polygon(
            self.screen,
            (200, 10, 10),
            arrow_points
        )
        
        # Маркер игрока
        pygame.draw.circle(
            self.screen,
            (150, 150, 150),
            (
                map_size[0] / 2,
                HEIGHT - map_size[0] / 2
            ),
            11
        )
        pygame.draw.circle(
            self.screen,
            (255, 255, 255),
            (
                map_size[0] / 2,
                HEIGHT - map_size[0] / 2
            ),
            10
        )
        font = pygame.font.SysFont('Arial', 16, bold=True)
        text = font.render(
            'Я',
            True,
            (200, 10, 10)
        )
        self.screen.blit(
            text,
            (
                (map_size[0] - text.get_rect().size[0]) / 2,
                HEIGHT - (map_size[0] + text.get_rect().size[1]) / 2
            )
        )
    
    def health_bar(self, player):
        self.rc.get('health_bar').set_value(player.health)
        self.rc.get('health_bar').draw(self.screen)

    def background(self, player):
        # Попытка сделать паралакс,
        # домножение на sin(vx + 90) и cos(vx + 90)
        # даёт возможность отделить перемещение влево/вправо
        # от перемещения вперёд/назад, но даёт негативный эффект
        # в виде перемещения неба в сторону поворота камерой
        # sky_offset = round(
        #     player.x * cos(radians(player.vx + 90)) +
        #     player.y * sin(radians(player.vx + 90))
        # )
        sky_offset = round(-player.vx / FOV * WIDTH)
        sky_size = self.rc.get('world_sky').get_rect().size
        sky_size = (
            round(sky_size[0] / sky_size[1] * HEIGHT / 2),
            HEIGHT // 2
        )
        sky = pygame.transform.scale(
            self.rc.get('world_sky'),
            sky_size
        )
        
        # Заполнения всей ширины экрана бесшовной текстурой неба
        for i in range(
            sky_offset % sky_size[0] - sky_size[0],
            WIDTH,
            sky_size[0]
        ):
            self.screen.blit(
                sky,
                (i, 0)
            )

        pygame.draw.rect(
            self.screen,
            (60, 60, 90),
            (0, HEIGHT // 2, WIDTH, HEIGHT // 2)
        )

    def world(self, world, player):
        z_buffer = []

        for sprite in world.sprite_group:
            sprite_distance = (
                (sprite.sprite_x - player.x) ** 2 +
                (sprite.sprite_y - player.y) ** 2
            ) ** 0.5

            z_buffer.append([
                sprite_distance,
                {
                    'type': type(sprite).__name__
                },
                sprite
            ])

        for i in range(RAYS_AMOUNT):
            ray_angle_x = player.vx + i * OFFSET_ANGLE - FOV / 2
            depth, ray_offset, obj_info = ray_cast(
                world,
                player.x,
                player.y,
                ray_angle_x
            )

            # Исправление эффекта рыбьего глаза
            depth *= cos(radians(player.vx - ray_angle_x))
            
            z_buffer.append([
                depth,
                obj_info,
                [
                    i, ray_offset
                ]
            ])

        for depth, obj_info, obj_data in sorted(
            z_buffer, key=lambda x: x[0], reverse=True
        ):
            if obj_info['type'] in ['WorldSprite', 'Enemy']:
                sprite = obj_data
                sprite.draw(self.screen)
            elif obj_info['type'] == 'Wall':
                i, ray_offset = obj_data

                # Высота проекции стены на экран
                wall_height = 5 * (DIST * GRID_SIZE) // \
                              (depth + 0.0001)

                pixel_color = [
                    max(
                        0,
                        min(
                            255,
                            255 - 255 * (depth / MAX_DEPTH)
                        )
                    )
                ] * 3

                pygame.draw.rect(
                    self.screen,
                    pixel_color,
                    (
                        i * WIDTH // RAYS_AMOUNT - 1,
                        (HEIGHT - wall_height) // 2,
                        WIDTH // RAYS_AMOUNT + 1,
                        wall_height
                    )
                )
            elif obj_info['type'] == 'TexturedWall':
                i, ray_offset = obj_data

                # Высота проекции стены на экран
                wall_height = 5 * (DIST * GRID_SIZE) // \
                              (depth + 0.0001)

                tile_scale = DIST / (depth + 0.0001)
                tile_scale = min(5, max(1, tile_scale))

                wall_column = self.rc.get(obj_info['texture_name'])
                texture_width, texture_height = wall_column.get_size()
                texture_scale_x = texture_width // GRID_SIZE

                # Вырезаем из текстуры столб пикселей
                wall_column = wall_column.subsurface(
                    round(ray_offset * texture_scale_x),
                    0,
                    texture_scale_x,
                    texture_height
                )

                # Растягиваем стоб пикселей в ширину,
                # чтобы не было видно стыков,
                # когда мы близко подходим к стене
                wall_column = pygame.transform.scale(
                    wall_column,
                    (
                        round(texture_scale_x * tile_scale),
                        texture_height
                    )
                )

                # Вырезаем из растянутой текстуры фрагмент,
                # с постоянным соотношением сторон
                wall_column = wall_column.subsurface(
                    0,
                    0,
                    texture_scale_x,
                    texture_height
                )

                # Растягиваем фрагмент текстуры,
                # чтобы он поместился на экран
                wall_column = pygame.transform.scale(
                    wall_column,
                    (
                        WIDTH // RAYS_AMOUNT + 1,
                        int(wall_height)
                    )
                )

                # Выводим фрагмент текстуры на экран
                self.screen.blit(
                    wall_column,
                    (
                        i * (WIDTH // RAYS_AMOUNT + 1),
                        (HEIGHT - wall_height) // 2
                    )
                )

    def menu(self, menu_screen='main'):
        action = ''
        menu_running = True
        clock = pygame.time.Clock()

        title_text = self.rc.get('title_text')
        start_button = self.rc.get('start_button')
        settings_button = self.rc.get('settings_button')
        exit_button = self.rc.get('exit_button')
        back_button = self.rc.get('back_button')

        background_image = pygame.transform.scale(
            self.rc.get('menu_background'),
            (WIDTH, HEIGHT)
        )

        while menu_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

            self.screen.blit(background_image, (0, 0))
            title_text.draw(self.screen)

            if menu_screen == 'main':
                for btn in [start_button, settings_button, exit_button]:
                    btn.update_state(pygame.mouse)

                    if btn.get_state() == 'clicked-mouseup':
                        self.rc.get('button_sound').play()

                        if id(btn) == id(start_button):
                            action = 'start_game'
                            menu_running = False
                        elif id(btn) == id(settings_button):
                            action = self.menu('settings')
                        elif id(btn) == id(exit_button):
                            action = 'exit'
                            menu_running = False

                    btn.draw(self.screen)
            elif menu_screen == 'settings':
                for slider_key in [
                    'music_volume', 'sound_volume', 'rays_amount'
                ]:
                    self.rc.get(slider_key + '_slider').update_state(
                        pygame.mouse
                    )

                    self.rc.get(slider_key + '_label').set_text(
                        str(
                            int(
                                self.rc.get(
                                    slider_key + '_slider'
                                ).get_value()
                            )
                        )
                    )

                    self.rc.get(slider_key + '_subtitle').draw(self.screen)
                    self.rc.get(slider_key + '_slider').draw(self.screen)
                    self.rc.get(slider_key + '_label').draw(self.screen)

                music_volume = self.rc.get(
                    'music_volume_slider'
                ).get_value() / 100

                sound_volume = self.rc.get(
                    'sound_volume_slider'
                ).get_value() / 100

                self.rc.get('game_music').set_volume(music_volume)
                self.rc.get('menu_music').set_volume(music_volume)
                self.rc.get('gun_sound').set_volume(sound_volume)

                back_button.update_state(pygame.mouse)
                back_button.draw(self.screen)
                if back_button.get_state() == 'clicked-mouseup':
                    self.rc.get('button_sound').play()
                    menu_running = False

            clock.tick(60)
            pygame.display.flip()

        return action

    def aim(self):
        aim_img = self.rc.get('aim')
        self.screen.blit(
            aim_img,
            (
                (WIDTH - aim_img.get_size()[0]) / 2,
                (HEIGHT - aim_img.get_size()[1]) / 2
            )
        )

    def weapon(self, weapon):
        img_original_width = self.rc.get(
            weapon.animations[weapon.state[0]][0][weapon.state[1]]
        ).get_size()[0]

        img = pygame.transform.scale(
            self.rc.get(
                weapon.animations[weapon.state[0]][0][weapon.state[1]]
            ),
            (WIDTH, HEIGHT)
        )
        self.screen.blit(
            img,
            (
                # Чтобы соотнести прицел и центр оружия
                -30 * WIDTH / img_original_width,
                0
            )
        )
