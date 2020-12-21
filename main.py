import pygame
from math import cos, sin, radians
from settings import *
from ray import Ray
from world import World
from player import Player
from drawing import Drawing

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Cosmic Occasion')

    size = WIDTH, HEIGHT
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
    
    draw = Drawing(screen)

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

        draw.background()
        draw.world(world, player)
        draw.fps(clock)

        pygame.display.flip()

    pygame.quit()