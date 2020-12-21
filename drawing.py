import pygame
from math import tan, cos, radians
from settings import *
from ray import Ray
from world import World
from player import Player

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

        for i in range(0, RAYS_AMOUNT):
            ray_angle_x = player.vx + (i - RAYS_AMOUNT // 2) * OFFSET_ANGLE
            depth, obj_info = ray.cast(
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