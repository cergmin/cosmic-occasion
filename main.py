from math import cos, sin, radians
import pygame
from pygame.mixer import Sound
from settings import *
from controllers import *
from world import *
from player import Player
from ray import ray_cast
from drawing import Drawing


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Cosmic Occasion')

    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)

    # Инициализация ресурсов
    ic = ImageController()
    for folder in ['normal', 'hover', 'clicked']:
        for img in ['start', 'between', 'middle', 'end']:
            ic.load(
                'images/button/' + folder + '/' + img + '.png',
                'btn_' + folder + '_' + img,
                alpha=True,
                max_height=100
            )

    for img in ['start', 'start_between', 'end_between', 'end', 'pointer']:
        ic.load(
            'images/slider/' + img + '.png',
            'slider_' + img,
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

    ic.load(
        'images/aim.png',
        'aim',
        alpha=True
    )

    ic.load(
        'images/gun/shoot/0.png',
        'gun',
        alpha=True
    )
    ic.load(
        'images/gun/aim_shoot/0.png',
        'aimed_gun',
        alpha=True
    )
    for i in range(1, 11):
        ic.load(
            f'images/gun/shoot/{i}.png',
            'shot_' + str(i),
            alpha=True
        )
    for i in range(11):
        ic.load(
            f'images/gun/aim/{i}.png',
            'aiming_' + str(i),
            alpha=True
        )
    for i in range(1, 11):
        ic.load(
            f'images/gun/aim_shoot/{i}.png',
            'aimed_shot_' + str(i),
            alpha=True
        )
    game_music = Sound('sounds/game.mp3')
    game_music.stop()

    menu_music = Sound('sounds/menu.mp3')
    menu_music.stop()

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
    gun = Weapon(
        ['gun'], ['aimed_gun'],
        ['shot_' + str(i) for i in range(1, 11)],
        ['aiming_' + str(i) for i in range(1, 11)],
        ['aimed_shot_' + str(i) for i in range(1, 11)],
        'sounds/gun.mp3',
        shot_duration=0.3,
        aiming_duration=0.2
    )

    draw = Drawing(screen, ic)
    clock = pygame.time.Clock()

    is_aiming = False
    menu_opened = True
    running = True
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

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    gun.sound.play()
                    gun.set_state(
                        'aimed_shot' if is_aiming else 'shot'
                    )
                elif event.button == 3:
                    is_aiming = not is_aiming
                    
                    if is_aiming:
                        gun.set_state('aiming')
                        player.speed /= 4
                        SENSITIVITY *= 4
                    else:
                        gun.set_state('reversed_aiming')
                        player.speed *= 4
                        SENSITIVITY /= 4

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.move(world, 0, player.speed * tick)
        if keys[pygame.K_s]:
            player.move(world, 180, player.speed * tick)
        if keys[pygame.K_a]:
            player.move(world, -90, player.speed * tick)
        if keys[pygame.K_d]:
            player.move(world, 90, player.speed * tick)
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
        draw.aim()
        gun.update(tick)
        draw.weapon(gun)

        pygame.display.flip()
    pygame.quit()
