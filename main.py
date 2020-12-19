import pygame


class World:
    def __init__(self, map):
        self.map = list(map)

    def get(self, x, y):
        return self.map[x][y]

    def set(self, x, y, obj):
        self.map[x][y] = obj

    def set_map(self, map):
        self.map = map


class Ray:
    def __init__(self, world):
        self.world = world

    def cast(self, pl_x, pl_y, deg_x, deg_y):
        return (255, 0, 0)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Cosmic Occasion')

    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)

    world = World([
        ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'],
        ['w', '.', '.', '.', '.', '.', '.', 'w'],
        ['w', '.', 'w', 'w', 'w', 'w', '.', 'w'],
        ['w', '.', '.', '.', '.', 'w', '.', 'w'],
        ['w', '.', '.', 'p', '.', '.', '.', 'w'],
        ['w', '.', '.', '.', '.', '.', '.', 'w'],
        ['w', '.', '.', '.', '.', '.', '.', 'w'],
        ['w', '.', '.', '.', '.', '.', '.', 'w'],
        ['w', '.', '.', '.', '.', '.', '.', 'w'],
        ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w']
    ])

    ray = Ray(world)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        for i in range(width):
            for j in range(height):
                pixel_color = ray.cast(0, 0, 0, 0)
                pygame.draw.rect(screen, pixel_color, (i, j, 1, 1))

        pygame.display.flip()

    pygame.quit()