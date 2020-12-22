import pygame
from math import tan, cos, radians
from settings import *
from ray import Ray


class Drawing:
    def __init__(self, screen):
        self.screen = screen

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
        text = font.render(fps_amount, 0, (255, 0, 0))
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
                texture_scale_y = texture_height // TILE_SIZE

                wall_column = obj_info['texture'].subsurface(ray_offset * texture_scale_x, 0, texture_scale_x, texture_height)
                wall_column = pygame.transform.scale(wall_column, (WIDTH // RAYS_AMOUNT, int(wall_height)))
                self.screen.blit(wall_column, (i * (WIDTH // RAYS_AMOUNT), (HEIGHT - wall_height) // 2))

                pixel_color = [
                                  max(0, min(255, 255 - 255 * (depth / MAX_DEPTH)))
                              ] * 3
