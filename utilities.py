from settings import *

def mapping(x, y):
    '''Возвращает координаты верхней левой точеи клетки,
       в которой находится точка (x, y)'''
    return (x // TILE_SIZE) * TILE_SIZE, (y // TILE_SIZE) * TILE_SIZE