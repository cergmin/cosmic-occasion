from math import radians, tan

GRID_SIZE = 60
WIDTH = 1280
HEIGHT = 720
RAYS_AMOUNT = 100

FOV = 60  # Угол зрения игрока
DIST = 60 / (2 * tan(radians(FOV / 2)))  # Расстояние от игрока до экрана
OFFSET_ANGLE = FOV / RAYS_AMOUNT
MAX_DEPTH = 780

SENSITIVITY = 10
