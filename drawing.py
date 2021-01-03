import pygame
import time
from math import tan, cos, radians
from settings import *
from ray import Ray
from pygame.mixer import Sound
from controllers import ImageController


class ElementUI:
    def __init__(self, x, y, width, height):
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


class Button(ElementUI):
    def __init__(self, x, y, width, height,
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
        super().__init__(x, y, width, height)

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
            'clicked',
        ]
        self.state = self.states_list[0]

    def set_state(self, state):
        state = str(state).lower()
        if state not in self.states_list:
            self.state = self.states_list[0]
        else:
            self.state = state

    def draw(self, surface):
        img_w = {}

        for i in filter(
            lambda x: x.startswith(self.state + '_'),
            self.img
        ):
            img_w[i.split('_')[-1]] = max(
                1,
                round(
                    self.img[i].get_size()[0] * \
                    (self.height / self.img[i].get_size()[1])
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
                self.img[self.state + '_' + i[0]],
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
            self.text_color[self.state]
        )
        surface.blit(
            text_surface,
            (
                self.x + (self.width - text_surface.get_size()[0]) // 2,
                self.y + (self.height - text_surface.get_size()[1]) // 2
            )
        )


class Drawing:
    def __init__(self, screen, ic):
        self.screen = screen
        self.ic = ic
        self.ray = Ray()

    def background(self):
        pygame.draw.rect(
            self.screen,
            (117, 187, 253),
            (0, 0, WIDTH, HEIGHT // 2)
        )
        pygame.draw.rect(
            self.screen,
            (40, 25, 15),
            (0, HEIGHT // 2, WIDTH, HEIGHT // 2)
        )

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

    def world(self, world, player):
        for i in range(RAYS_AMOUNT):
            ray_angle_x = player.vx + i * OFFSET_ANGLE - FOV / 2
            depth, ray_offset, obj_info = self.ray.cast(
                world,
                player.x,
                player.y,
                ray_angle_x
            )

            # Исправление эффекта рыбьего глаза
            depth *= cos(radians(player.vx - ray_angle_x))

            if obj_info['type'] == 'Wall':
                # Высота проекции стены на экран
                wall_height = 5 * (DIST * TILE_SIZE) // \
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
                # Высота проекции стены на экран
                wall_height = 5 * (DIST * TILE_SIZE) // \
                              (depth + 0.0001)

                tile_scale = DIST / (depth + 0.0001)
                tile_scale = min(5, max(1, tile_scale))

                wall_column = self.ic.get(obj_info['texture_name'])
                texture_width, texture_height = wall_column.get_size()
                texture_scale_x = texture_width // TILE_SIZE

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
                        WIDTH // RAYS_AMOUNT,
                        int(wall_height)
                    )
                )

                # Выводим фрагмент текстуры на экран
                self.screen.blit(
                    wall_column,
                    (
                        i * (WIDTH // RAYS_AMOUNT),
                        (HEIGHT - wall_height) // 2
                    )
                )

    def menu(self):
        clock = pygame.time.Clock()
        self.menu_running = True

        button_resources = []
        for folder in ['normal', 'hover', 'clicked']:
            for img in ['start', 'between', 'middle', 'end']:
                button_resources.append(
                    self.ic.get('btn_' + folder + '_' + img)
                )

        button_text_attributes = {
            'text_color': (171, 242, 255),
            'text_color_hover': (194, 244, 255),
            'text_color_clicked': (143, 201, 213),
            'font': pygame.font.Font('font/guardiane.ttf', 40)
        }

        start_button = Button(
            WIDTH // 2 - 210, 250, 420, 100,
            *button_resources,
            **button_text_attributes,
            text='start'
        )

        settings_button = Button(
            WIDTH // 2 - 210, 370, 420, 100,
            *button_resources,
            **button_text_attributes,
            text='settings'
        )

        exit_button = Button(
            WIDTH // 2 - 210, 490, 420, 100,
            *button_resources,
            **button_text_attributes,
            text='exit'
        )

        title_font = pygame.font.Font('font/guardianlai.ttf', WIDTH // 13)
        title = title_font.render('COSMIC OCCASION', True, (255, 255, 255))

        background_image = pygame.transform.scale(
            self.ic.get('menu_background'),
            (WIDTH, HEIGHT)
        )

        mouse_state = [False, -1]  # [is_clicked, btn_id]
        while self.menu_running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

            self.screen.blit(background_image, (0, 0))

            self.screen.blit(
                title,
                (
                    (WIDTH - title.get_size()[0]) // 2,
                    (200 - title.get_size()[1]) // 2
                )
            )
            for btn in [start_button, settings_button, exit_button]:
                if btn.is_hover(*pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed(3)[0]:
                        btn.set_state('clicked')
                        mouse_state[1] = id(btn)
                    else:
                        btn.set_state('hover')
                else:
                    btn.set_state('normal')
                btn.draw(self.screen)
            mouse_state[0] = pygame.mouse.get_pressed(3)[0]
            if not mouse_state[0]:
                if mouse_state[1] != -1:
                    Sound("sounds/button_pressed.mp3").play()

                if mouse_state[1] == id(start_button):
                    self.menu_running = False
                elif mouse_state[1] == id(settings_button):
                    print('settings')
                elif mouse_state[1] == id(exit_button):
                    pygame.quit()
                    exit(0)

                mouse_state[1] = -1

            clock.tick(60)
            pygame.display.flip()

    def aim(self):
        aim_img = self.ic.get('aim')
        self.screen.blit(
            aim_img,
            (
                (WIDTH - aim_img.get_size()[0]) / 2,
                (HEIGHT - aim_img.get_size()[1]) / 2
            )
        )

    def weapon(self, weapon):
        img_original_width = self.ic.get(
            weapon.animations[weapon.state[0]][0][weapon.state[1]]
        ).get_size()[0]

        img = pygame.transform.scale(
            self.ic.get(
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
