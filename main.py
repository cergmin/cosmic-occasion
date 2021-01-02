import pygame
from math import cos, sin, radians
from settings import *
from controllers import *
from world import World
from player import Player
from drawing import Drawing
from pygame.mixer import Sound


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Cosmic Occasion')

    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)

    ic = ImageController()

    player = Player(100, 100)
    world = World([
        ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'],
        ['w', '.', '.', '.', '.', '.', '.', 'w'],
        ['w', 'w', 'w', 'w', '.', 'w', '.', 'w'],
        ['w', '.', '.', 'w', '.', 'w', '.', 'w'],
        ['w', '.', '.', 'w', '.', 'w', '.', 'w'],
        ['w', '.', '.', 'w', '.', 'w', 'w', 'w'],
        ['w', '.', '.', '.', '.', '.', '.', 'w'],
        ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w']
    ])


    draw = Drawing(screen, ic)
    clock = pygame.time.Clock()

    # Инициализация ресурсов
    for folder in ['normal', 'hover', 'clicked']:
        for img in ['start', 'between', 'middle', 'end']:
            ic.load(
                'images/button/' + folder + '/' + img + '.png',
                'btn_' + folder + '_' + img,
                alpha=True,
                max_height=100
            )

    ic.load(
        'images/menu.jpg',
        'menu_background',
        max_width=WIDTH,
        max_height=HEIGHT
    )

    ic.load(
        'images/wall.jpg',
        'wall'
    )

    game_music = Sound('sounds/game.mp3')
    game_music.stop()

    menu_music = Sound('sounds/menu.mp3')
    menu_music.stop()
    shot = False
    menu_opened = True
    running = True
    while running:
        triggered = False
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Sound("sounds/gun.mp3").play()
                    shot = True
                    triggered = True
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
            menu_opened = True

        if menu_opened:
            # Показываем и "отпускаем" курсор
            pygame.mouse.set_visible(True)
            pygame.event.set_grab(False)

            # Переключение фоновой музыки
            game_music.stop()
            menu_music.play(loops=-1)

            # Установка курсора в центр и открытие меню
            pygame.mouse.set_pos(WIDTH // 2, HEIGHT // 2)
            draw.menu()

            # Прячем и "захватываем" курсор
            pygame.mouse.set_visible(False)
            pygame.event.set_grab(True)

            # Переключение фоновой музыки
            game_music.play(loops=-1)
            menu_music.stop()

            menu_opened = False

        draw.background()
        draw.world(world, player)
        draw.fps(clock)
        if draw.gun(shot):
            shot = False
        draw.aim(triggered)
        pygame.display.flip()

    pygame.quit()
