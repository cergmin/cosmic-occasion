from math import *

TILE_SIZE = 64
WIDTH = 1280
HEIGHT = 720
RAYS_AMOUNT = 90

FOV = 60  # Угол зрения игрока
DIST = 60 / (2 * tan(radians(FOV / 2)))  # Расстояние от игрока до экрана
OFFSET_ANGLE = FOV / RAYS_AMOUNT
MAX_DEPTH = 500

SENSITIVITY = 10
