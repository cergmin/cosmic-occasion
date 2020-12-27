import pygame
from math import tan, cos, radians
from settings import *
from ray import Ray


class Drawing:
    def __init__(self, screen):
        self.screen = screen
        self.menu_running = True
        self.menu_picture = pygame.transform.scale(pygame.image.load('images/menu.jpg').convert(), (WIDTH, HEIGHT))
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

        last_depth = None
        last_wall_height = None
        for i in range(0, RAYS_AMOUNT):
            ray_angle_x = player.vx + (i - RAYS_AMOUNT // 2) * OFFSET_ANGLE
            depth, ray_offset, obj_info = ray.cast(
                player.x,
                player.y,
                ray_angle_x + 25,
                player.vy
            )

            # Исправление эффекта рыбьего глаза
            depth *= cos(radians(player.vx - ray_angle_x))

            # Расстояние от игрока до экрана
            dist = RAYS_AMOUNT / (2 * tan(radians(FOV / 2)))

            if obj_info['type'] == 'Wall':
                # Высота проекции стены на экран
                wall_height = 5 * (dist * obj_info['height']) // \
                              (depth + 0.0001)

                pixel_color = [
                                  max(0, min(255, 255 - 255 * (depth / MAX_DEPTH)))
                              ] * 3

                if last_depth is not None and \
                        abs(depth - last_depth) < SMOTHING_THRESHOLD:
                    pygame.draw.polygon(
                        self.screen,
                        pixel_color,
                        (
                            (
                                i * WIDTH // RAYS_AMOUNT - 1,
                                (HEIGHT - last_wall_height) // 2
                            ),
                            (
                                (i + 1) * WIDTH // RAYS_AMOUNT,
                                (HEIGHT - wall_height) // 2
                            ),
                            (
                                (i + 1) * WIDTH // RAYS_AMOUNT,
                                (HEIGHT - wall_height) // 2 + wall_height
                            ),
                            (
                                i * WIDTH // RAYS_AMOUNT - 1,
                                (HEIGHT - last_wall_height) // 2 + last_wall_height
                            )
                        )
                    )
                else:
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

                last_depth = depth
                last_wall_height = wall_height
            elif obj_info['type'] == 'TexturedWall':
                # Высота проекции стены на экран
                wall_height = 5 * (dist * obj_info['height']) // \
                              (depth + 0.0001)

                ray_offset = int(ray_offset) % TILE_SIZE

                texture_width, texture_height = obj_info['texture'].get_size()
                texture_scale_x = texture_width // TILE_SIZE

                wall_column = obj_info['texture'].subsurface(ray_offset * texture_scale_x, 0, texture_scale_x,
                                                             texture_height)
                wall_column = pygame.transform.scale(wall_column, (WIDTH // RAYS_AMOUNT, int(wall_height)))
                self.screen.blit(wall_column, (i * (WIDTH // RAYS_AMOUNT), (HEIGHT - wall_height) // 2))

    def menu(self):

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
