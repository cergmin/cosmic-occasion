from settings import *

def mapping(x, y):
    '''Возвращает координаты верхней левой точеи клетки,
       в которой находится точка (x, y)'''
    return (x // GRID_SIZE) * GRID_SIZE, (y // GRID_SIZE) * GRID_SIZE