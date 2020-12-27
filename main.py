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
    draw.menu()
    running = True
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    while running:
        tick = clock.tick() / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEMOTION:
                # Если mouse.get_visible() = False и event.set_grab(True),
                # то метод mouse.set_pos(...) не работает
                if pygame.mouse.get_visible():
                    player.vx += (event.pos[0] - WIDTH // 2) * (1 / SENSITIVITY)
                    pygame.mouse.set_pos(WIDTH // 2, HEIGHT // 2)
                else:
                    player.vx += event.rel[0] * (1 / SENSITIVITY)

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
        if keys[pygame.K_ESCAPE]:
            running = False

        draw.background()
        draw.world(world, player)
        draw.fps(clock)

        # Рисование прицела
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (WIDTH // 2 - 2, HEIGHT // 2 - 2, 14, 14)
        )
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (WIDTH // 2, HEIGHT // 2, 10, 10)
        )

        pygame.display.flip()

    pygame.quit()
