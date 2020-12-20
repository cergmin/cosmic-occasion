import pygame
from math import tan, cos, radians
from settings import *
from ray import Ray
from world import World
from player import Player

class Drawing:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = self.screen.get_size()

    def background(self):
        pygame.draw.rect(
            self.screen,
            (117, 187, 253),
            (0, 0, self.width, self.height // 2)
        )
        pygame.draw.rect(
            self.screen,
            (40, 25, 15),
            (0, self.height // 2, self.width, self.height // 2)
        )
    
    def fps(self, clock):
        fps_amount = str(int(clock.get_fps()))
        font = pygame.font.SysFont('Arial', 36, bold=True)
        text = font.render(fps_amount, 0, (255, 0, 0))
        self.screen.blit(
            text,
            (
                self.width - text.get_size()[0] - 7,
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
                ray_angle_x,
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
                    255 - 255 * (depth / MAX_DEPTH)
                ] * 3

                pygame.draw.rect(
                    self.screen,
                    pixel_color,
                    (
                        i * self.width // RAYS_AMOUNT - 1,
                        (self.height - wall_height) // 2,
                        self.width // RAYS_AMOUNT + 1,
                        wall_height
                    )
                )