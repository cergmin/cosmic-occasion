from math import cos, sin, radians
from random import randint
from multiprocessing import Event
import threading
import pygame
from settings import *
from utilities import *
from controllers import *
from world import *
from player import Player
from ray import ray_cast
from drawing import *


def loading_resources(kill_event):
    rc.load('game_music', 'sounds/game.mp3')
    rc.load('menu_music', 'sounds/menu.mp3')
    rc.load('gun_sound', 'sounds/gun.mp3')
    rc.load('hit_sound', 'sounds/hit.mp3')
    rc.load('button_sound', 'sounds/button_pressed.mp3')

    rc.load(
        'font_guardianlai_w/14',
        pygame.font.Font('font/guardianlai.ttf', WIDTH // 14)
    )
    rc.load(
        'font_RussoOne_w/20',
        pygame.font.Font('font/RussoOne.ttf', WIDTH // 20)
    )
    rc.load(
        'font_RussoOne_40',
        pygame.font.Font('font/RussoOne.ttf', 40)
    )
    rc.load(
        'font_Jura_22',
        pygame.font.Font('font/Jura.ttf', 22)
    )
    rc.load(
        'font_Jura_36',
        pygame.font.Font('font/Jura.ttf', 36)
    )

    rc.load(
        'title_text',
        Text(
            rc,
            0, 0, WIDTH, WIDTH // 7,
            text='COSMIC OCCASION',
            text_color=(255, 255, 255),
            font=rc.get('font_guardianlai_w/14')
        )
    )

    button_resources = []
    for folder in ['normal', 'hover', 'clicked']:
        for img in ['start', 'between', 'middle', 'end']:
            button_resources.append('btn_' + folder + '_' + img)

    button_text_attributes = {
        'text_color': (171, 242, 255),
        'text_color_hover': (194, 244, 255),
        'text_color_clicked': (143, 201, 213),
        'font': rc.get('font_RussoOne_40')
    }

    for i, (button_key, button_text) in enumerate([
        ('start_button', 'НАЧАТЬ'),
        ('settings_button', 'НАСТРОЙКИ'),
        ('exit_button', 'ВЫХОД'),
        ('back_button', 'НАЗАД')
    ]):
        rc.load(
            button_key,
            Button(
                rc,
                WIDTH // 2 - 210, WIDTH // 7 + 120 * i, 420, 100,
                *button_resources,
                **button_text_attributes,
                text=button_text
            )
        )


    for i, (key, subtitle, min_value, max_value, cur_value) in enumerate([
        ('music_volume', 'Громкость музыки', 0, 100, 100),
        ('sound_volume', 'Громкость звуков', 0, 100, 100),
        ('rays_amount', 'Количество лучей', 30, 600, 100)
    ]):
        block_margin = 100
        block_width = 420
        slider_margin = 50
        slider_width = 345
        rc.load(
            key + '_subtitle',
            Text(
                rc,
                (WIDTH - block_width) // 2,
                WIDTH // 7 + i * block_margin,
                block_width,
                50,
                text=subtitle,
                font=rc.get('font_Jura_22'),
                align='left'
            )
        )
        rc.load(
            key + '_slider',
            Slider(
                rc,
                (WIDTH - block_width) // 2,
                WIDTH // 7 + slider_margin + i * block_margin,
                slider_width,
                35,
                'slider_start',
                'slider_start_between',
                'slider_end_between',
                'slider_end',
                'slider_pointer',
                min_value=min_value,
                max_value=max_value,
                current_value=cur_value
            )
        )
        rc.load(
            key + '_label',
            Text(
                rc,
                (WIDTH - block_width) // 2 + slider_width + 5,
                WIDTH // 7 + slider_margin + i * block_margin,
                block_width - slider_width - 5,
                35,
                text='0',
                font=rc.get('font_Jura_22'),
                align='left'
            )
        )
    
    rc.load(
        'health_bar_full',
        'images/health_bar/full.png',
        alpha=True
    )
    rc.load(
        'health_bar_empty',
        'images/health_bar/empty.png',
        alpha=True
    )
    rc.load(
        'health_bar_pointer',
        'images/health_bar/pointer.png',
        alpha=True
    )
    
    rc.load(
        'health_bar',
        Bar(
            rc,
            -9,
            HEIGHT - 220,
            218,
            40,
            'health_bar_full',
            'health_bar_empty',
            'health_bar_pointer',
            min_value=0,
            max_value=PLAYER_MAX_HEALTH
        )
    )

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
        'score_card',
        'images/score_card.png',
        alpha=True
    )
    
    rc.load(
        'world_sky',
        'images/sky.jpg',
        max_height=(HEIGHT // 2)
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

    rc.load(
        'enemy_biba_normal_0',
        f'images/enemies/biba/normal/0.png',
        alpha=True
    )
    
    for i in range(20):
        rc.load(
            'enemy_biba_attack_' + str(i),
            f'images/enemies/biba/attack/{i}.png',
            alpha=True
        )
    
    kill_event.set()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Cosmic Occasion')

    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)

    # Инициализация ресурсов
    max_resources_amount = 104
    rc = ResourceController()

    kill_event = Event()
    loading_resources_thread = threading.Thread(
        target=loading_resources,
        args=(kill_event, )
    )
    loading_resources_thread.setDaemon(True)
    loading_resources_thread.start()

    while not kill_event.is_set():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if rc.is_exists('menu_background'):
            background_image = pygame.transform.scale(
                rc.get('menu_background'),
                (WIDTH, HEIGHT)
            )
            screen.blit(background_image, (0, 0))
        else:
            pygame.draw.rect(
                screen,
                (10, 20, 40),
                (0, 0, WIDTH, HEIGHT)
            )

        if rc.is_exists('font_RussoOne_w/20'):
            font = rc.get('font_RussoOne_w/20')
        else:
            font = pygame.font.SysFont('Arial', WIDTH // 19, bold=True)

        text_a = font.render(
            'Загрузка ресурсов',
            False,
            (255, 255, 255)
        )
        text_b = font.render(
            str(len(rc.resources)) + '/' + str(max_resources_amount),
            False,
            (255, 255, 255)
        )

        screen.blit(
            text_a,
            (
                (WIDTH - text_a.get_size()[0]) / 2,
                50
            )
        )
        screen.blit(
            text_b,
            (
                (WIDTH - text_b.get_size()[0]) / 2,
                70 + text_a.get_size()[1]
            )
        )

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (
                WIDTH / 10,
                90 + text_a.get_size()[1] + text_b.get_size()[1],
                WIDTH * 8 / 10,
                WIDTH / 20
            ),
            width=3
        )
        pygame.draw.rect(
            screen,
            (23, 147, 229),
            (
                WIDTH / 10 + 5,
                90 + text_a.get_size()[1] + text_b.get_size()[1] + 5,
                (WIDTH * 8 / 10 - 10) * (
                    len(rc.resources) / max_resources_amount
                ),
                WIDTH / 20 - 10
            )
        )

        pygame.display.flip()

    player = Player(100, 330, health=PLAYER_MAX_HEALTH)
    world = World('''
        wwwwwwwwwwwwwwwwwwwww
        w.w.............w...w
        w.w.w.wwwww.www.w.www
        w...w.ww.....w......w
        wwwww.ww.....w.www.ww
        w......w.....w.w...ww
        wwwww.wwww.www.w.wwww
        w.w.w.w....w...w....w
        w...w.wwww.w.wwwwww.w
        w..........w........w
        wwwwwwwwwwwwwwwwwwwww
    ''')

    gun = Weapon(
        WeaponBullet(90),
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
    
    score = 0
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

                    gun.bullet.recover()
                    world.update_sprites(
                        player, 0, 
                        shot=True,
                        weapon_bullet=gun.get_bullet(),
                        bullet_max_distance=ray_cast(
                            world,
                            player.x,
                            player.y,
                            player.vx
                        )[0]
                    )

                    power_used = gun.bullet.get_max_power() - \
                                 gun.bullet.get_power()

                    score += power_used / 100

                elif event.button == 3:
                    is_aiming = not is_aiming
                    
                    if is_aiming:
                        gun.set_state('aiming')
                        player.speed /= 2.5
                        SENSITIVITY *= 2.5
                    else:
                        gun.set_state('reversed_aiming')
                        player.speed *= 2.5
                        SENSITIVITY /= 2.5

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

        # Растущая от score сложность (в виде увеличения количества врагов)
        max_enemies_amount = 20 + int(score * (score + 3) / (score + 2))

        # Поддержание количества врагов на определённом значении
        for i in range(max_enemies_amount - len(world.sprite_group)):
            while True:
                y = randint(0, len(world.map) - 1)
                x = randint(0, len(world.map[y]) - 1)
    
                if is_cell_empty(
                    x, y, world.map,
                    busy_cells=get_cells_around(
                        *mapping(player.x, player.y),
                        radius=3
                    )
                ):
                    x *= GRID_SIZE
                    x += GRID_SIZE / 2
                    y *= GRID_SIZE
                    y += GRID_SIZE / 2
                    break
            
            world.add_sprite(
                AnimatedEnemy(
                    x, y, 350,
                    {
                        'normal': ['enemy_biba_normal_0'],
                        'attack': [
                            'enemy_biba_attack_' + str(i)
                            for i in range(20)
                        ]
                    },
                    'hit_sound',
                    rc,
                    health=100,
                    damage=20,
                    speed=50,
                    visibility_distance=300,
                    collider_width='93%',
                    collider_offset='5%'
                )
            )

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
            world.update_sprites(player, tick)

            draw.background(player)
            draw.world(world, player)
            draw.fps(clock)
            draw.aim()
            draw.minimap(world, player)
            draw.health_bar(player)
            draw.score_card(int(score))

            gun.update(tick)
            draw.weapon(gun)

            if player.health <= 0:
                # Открытие экрана смерти
                pygame.mouse.set_visible(True)
                pygame.event.set_grab(False)
                rc.get('game_music').stop()
                rc.get('menu_music').stop()
                pygame.mouse.set_pos(WIDTH // 2, HEIGHT // 2)
                draw.menu(menu_screen='death', score=int(score))

                # Обнуление игры
                player.health = player.max_health
                player.x = 100
                player.y = 330
                player.vx = 0

                for sprite in world.sprite_group:
                    world.sprite_group.remove(sprite)
                
                
                # Открытие главного меню
                menu_opened = True
                
        pygame.display.flip()
    pygame.quit()
