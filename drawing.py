import pygame
from math import tan, cos, radians
from settings import *
from ray import Ray


class Drawing:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()

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
        ray = Ray(world, player)

        for i in range(RAYS_AMOUNT):
            ray_angle_x = player.vx + i * OFFSET_ANGLE - FOV / 2
            depth, ray_offset, obj_info = ray.cast(
                player.x,
                player.y,
                ray_angle_x,
                player.vy
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
                texture_width, texture_height = obj_info['texture'].get_size()
                texture_scale_x = texture_width // TILE_SIZE

                # Высота проекции стены на экран
                wall_height = 5 * (DIST * TILE_SIZE) // \
                              (depth + 0.0001)

                tile_scale = DIST / (depth + 0.0001)
                tile_scale = max(1, tile_scale)

                wall_column = obj_info['texture']

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
        self.menu_running = True
        self.menu_picture = pygame.transform.scale(pygame.image.load('images/menu.jpg').convert(), (WIDTH, HEIGHT))
        button_font = pygame.font.Font('font/guardiane.ttf', WIDTH // 30)
        name_font = pygame.font.Font('font/guardianlai.ttf', WIDTH // 13)
        size_name = name_font.size("COSMIC OCCASION")

        button_start = pygame.Rect(0, 0, WIDTH // 4, HEIGHT // 5)
        button_start.center = WIDTH // 2, HEIGHT // 2
        size_start = button_font.size('START')

        button_exit = pygame.Rect(0, 0, WIDTH // 4, HEIGHT // 5)
        button_exit.center = WIDTH // 2, HEIGHT // 2 + HEIGHT // 4
        size_exit = button_font.size('EXIT')

        while self.menu_running:
            start_font = button_font.render('START', True, pygame.Color('white'))
            exit_font = button_font.render('EXIT', True, pygame.Color('white'))

            for event in pygame.event.get():
                if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    pygame.quit()
            self.screen.blit(self.menu_picture, (0, 0))

            pygame.draw.rect(self.screen, pygame.Color("black"), button_start, border_radius=30)
            pygame.draw.rect(self.screen, pygame.Color("white"), button_start, border_radius=30, width=10)
            self.screen.blit(start_font,
                             (button_start.centerx - size_start[0] / 2, button_start.centery - size_start[1] / 2))

            pygame.draw.rect(self.screen, pygame.Color("black"), button_exit, border_radius=30)
            pygame.draw.rect(self.screen, pygame.Color("white"), button_exit, border_radius=30, width=10)
            self.screen.blit(exit_font,
                             (button_exit.centerx - size_exit[0] / 2, button_exit.centery - size_exit[1] / 2))

            name = name_font.render('COSMIC OCCASION', True, pygame.Color("white"))
            self.screen.blit(name, (WIDTH // 2 - size_name[0] / 2, HEIGHT // 4 - size_name[0] / 8))

            if button_start.collidepoint(pygame.mouse.get_pos()):
                start_font = button_font.render('START', True, pygame.Color('black'))
                pygame.draw.rect(self.screen, pygame.Color("white"), button_start, border_radius=30)
                pygame.draw.rect(self.screen, pygame.Color("black"), button_start, border_radius=30, width=10)
                self.screen.blit(start_font,
                                 (button_start.centerx - size_start[0] / 2, button_start.centery - size_start[1] / 2))
                if pygame.mouse.get_pressed(3)[0]:
                    self.menu_running = False
            elif button_exit.collidepoint(pygame.mouse.get_pos()):
                exit_font = button_font.render('EXIT', True, pygame.Color('black'))
                pygame.draw.rect(self.screen, pygame.Color("white"), button_exit, border_radius=30)
                pygame.draw.rect(self.screen, pygame.Color("black"), button_exit, border_radius=30, width=10)
                self.screen.blit(exit_font,
                                 (button_exit.centerx - size_exit[0] / 2, button_exit.centery - size_exit[1] / 2))
                if pygame.mouse.get_pressed(3)[0]:
                    pygame.quit()

            self.clock.tick(60)
            pygame.display.flip()

    def aim(self):
        pygame.draw.rect(
            self.screen,
            (0, 0, 0),
            (WIDTH // 2 - 2, HEIGHT // 2 - 2, 14, 14)
        )
        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            (WIDTH // 2, HEIGHT // 2, 10, 10)
        )