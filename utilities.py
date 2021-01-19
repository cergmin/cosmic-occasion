from settings import *


def mapping(x, y):
    '''Возвращает координаты верхней левой точеи клетки,
       в которой находится точка (x, y)'''
    return (x // GRID_SIZE) * GRID_SIZE, (y // GRID_SIZE) * GRID_SIZE


def get_cells_around(x, y, radius=1):
    '''Возвращает список координат клеток вокруг (x, y)
       от (x - radius / 2, y - radius / 2)
       до (x + radius / 2, y + radius / 2)'''

    cells = []
    for x in range(int(x - radius / 2), int(x + radius / 2) + 1):
        for y in range(int(y - radius / 2), int(y + radius / 2) + 1):
            cells.append((x, y))

    return cells


def is_cell_empty(x, y, map, empty_chars=['.'], busy_cells=[]):
    return map[y][x] in empty_chars and (x, y) not in busy_cells
