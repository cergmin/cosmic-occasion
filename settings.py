from math import radians, tan

GRID_SIZE = 60
WIDTH = 1280
HEIGHT = 720
RAYS_AMOUNT = 100

FOV = 60  # Угол зрения игрока
DIST = 60 / (2 * tan(radians(FOV / 2)))  # Расстояние от игрока до экрана
MAX_DEPTH = 780  # Максимальная дальность прорисовки

SENSITIVITY = 10
PLAYER_MAX_HEALTH = 1000

DEFAULT_MUSIC_VOLUME = 50
DEFAULT_SOUND_VOLUME = 75
