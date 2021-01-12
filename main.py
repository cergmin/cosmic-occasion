from math import cos, sin, radians
import pygame
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
    rc = ResourceController()

    rc.load('game_music', 'sounds/game.mp3')
    rc.load('menu_music', 'sounds/menu.mp3')
    rc.load('gun_sound', 'sounds/gun.mp3')

    for folder in ['normal', 'hover', 'clicked']:
        for img in ['start', 'between', 'middle', 'end']:
            rc.load(
                'btn_' + folder + '_' + img,
                'images/button/' + folder + '/' + img + '.png',
                alpha=True,
                max_height=100
            )

    for img in ['start', 'start_between', 'end_between', 'end', 'pointer']:
        rc.load(
            'slider_' + img,
            'images/slider/' + img + '.png',
            alpha=True,
            max_height=100
        )

    rc.load(
        'menu_background',
        'images/menu.jpg',
        max_width=WIDTH,
        max_height=HEIGHT
    )

    rc.load(
        'wall',
        'images/wall.jpg'
    )

    rc.load(
        'aim',
        'images/aim.png',
        alpha=True
    )

    rc.load(
        'gun',
        'images/gun/shoot/0.png',
        alpha=True
    )

    rc.load(
        'aimed_gun',
        'images/gun/aim_shoot/0.png',
        alpha=True
    )

    for i in range(1, 11):
        rc.load(
            'shot_' + str(i),
            f'images/gun/shoot/{i}.png',
            alpha=True
        )

    for i in range(11):
        rc.load(
            'aiming_' + str(i),
            f'images/gun/aim/{i}.png',
            alpha=True
        )

    for i in range(1, 11):
        rc.load(
            'aimed_shot_' + str(i),
            f'images/gun/aim_shoot/{i}.png',
            alpha=True
        )
    
    rc.load('sprite', 'images/sprite.png', alpha=True)

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
    
    world.add_sprite(
        WorldSprite(
            300, 100, 350, 'sprite', rc
        )
    )

    world.add_sprite(
        WorldSprite(
            300, 400, 350, 'sprite', rc
        )
    )

    gun = Weapon(
        ['gun'], ['aimed_gun'],
        ['shot_' + str(i) for i in range(1, 11)],
        ['aiming_' + str(i) for i in range(1, 11)],
        ['aimed_shot_' + str(i) for i in range(1, 11)],
        'gun_sound',
        shot_duration=0.3,
        aiming_duration=0.2
    )

    draw = Drawing(screen, rc)
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
                    rc.get(gun.sound).play()
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
            rc.get('game_music').stop()
            rc.get('menu_music').play(loops=-1)

            # Установка курсора в центр и открытие меню
            pygame.mouse.set_pos(WIDTH // 2, HEIGHT // 2)
            action = draw.menu()

            if action == 'start_game':
                menu_opened = False
            elif action == 'exit':
                running = False
                menu_opened = False

            # Прячем и "захватываем" курсор
            pygame.mouse.set_visible(False)
            pygame.event.set_grab(True)

            # Переключение фоновой музыки
            rc.get('game_music').play(loops=-1)
            rc.get('menu_music').stop()
        else:
            draw.background()
            draw.world(world, player)
            draw.fps(clock)
            draw.aim()
            gun.update(tick)
            draw.weapon(gun)

        pygame.display.flip()
    pygame.quit()
