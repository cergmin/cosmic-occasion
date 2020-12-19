import pygame
from math import cos, sin, radians
from settings import *
from ray import Ray
from world import World
from player import Player

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Cosmic Occasion')

    size = width, height = 1280, 720
    screen = pygame.display.set_mode(size)

    player = Player(100, 100)
    world = World([
        ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'],
        ['w', '.', '.', '.', '.', '.', '.', 'w'],
        ['w', '.', 'w', 'w', 'w', 'w', '.', 'w'],
        ['w', '.', '.', '.', '.', 'w', '.', 'w'],
        ['w', '.', '.', '.', '.', '.', '.', 'w'],
        ['w', '.', '.', '.', '.', '.', '.', 'w'],
        ['w', '.', '.', '.', '.', '.', '.', 'w'],
        ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w']
    ])
    ray = Ray(world, screen, player)

    running = True
    clock = pygame.time.Clock()
    while running:
        tick = clock.tick() / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.x += player.speed * cos(radians(player.vx)) * tick
            player.y += player.speed * sin(radians(player.vx)) * tick
        if keys[pygame.K_s]:
            player.x -= player.speed * cos(radians(player.vx)) * tick
            player.y -= player.speed * sin(radians(player.vx)) * tick
        if keys[pygame.K_a]:
            player.x += player.speed * sin(radians(player.vx)) * tick
            player.y -= player.speed * cos(radians(player.vx)) * tick
        if keys[pygame.K_d]:
            player.x -= player.speed * sin(radians(player.vx)) * tick
            player.y += player.speed * cos(radians(player.vx)) * tick
        if keys[pygame.K_LEFT]:
            player.vx -= 80 * tick
        if keys[pygame.K_RIGHT]:
            player.vx += 80 * tick

        screen.fill((0, 0, 0))
        
        # pygame.draw.circle(
        #     screen,
        #     (255, 50, 130),
        #     (player.x, player.y),
        #     10
        # )
        # for obj in world.objects:
        #     pygame.draw.rect(
        #         screen,
        #         (50, 200, 50),
        #         (
        #             obj.x,
        #             obj.y,
        #             TILE_SIZE,
        #             TILE_SIZE
        #         ),
        #         2
        #     )
        
        for i in range(0, RAYS_AMOUNT):
            ray_angle_x = player.vx + (i - RAYS_AMOUNT // 2) * OFFSET_ANGLE
            ray_length = ray.cast(
                player.x,
                player.y,
                ray_angle_x + 20,
                player.vy
            )

            pixel_color = [
                round(255 - ray_length / MAX_DEPTH * 255)
            ] * 3

            wall_height = (MAX_DEPTH - ray_length) / MAX_DEPTH * height / 1.2

            pygame.draw.rect(
                screen,
                pixel_color,
                (
                    i * width // RAYS_AMOUNT - 1,
                    (height - wall_height) // 2,
                    width // RAYS_AMOUNT + 1,
                    wall_height
                )
            )

        pygame.display.flip()

    pygame.quit()