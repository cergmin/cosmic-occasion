import pygame
from math import cos, sin, radians
from settings import *
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
        ['w', '.', 'w', '.', '.', 'w', '.', 'w'],
        ['w', '.', 'w', '.', '.', 'w', '.', 'w'],
        ['w', '.', 'w', '.', '.', 'w', '.', 'w'],
        ['w', '.', '.', '.', '.', '.', '.', 'w'],
        ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w']
    ])

    draw = Drawing(screen)

    running = True
    is_cursor_event_odd = False
    pygame.mouse.set_visible(False)
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

        rel_move = pygame.mouse.get_rel()
        if rel_move[0] != 0:
            if is_cursor_event_odd:
                print(rel_move)
                player.vx += rel_move[0] * (1 / SENSITIVITY)
                pygame.mouse.set_pos(WIDTH // 2, HEIGHT // 2)
            is_cursor_event_odd = not is_cursor_event_odd

        draw.background()
        draw.world(world, player)
        draw.fps(clock)

        pygame.draw.rect(screen, (255, 0, 0), (WIDTH // 2, HEIGHT // 2, 10, 10))

        pygame.display.flip()

    pygame.quit()
