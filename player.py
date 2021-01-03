from settings import *


class Player:
    def __init__(self, x, y, vx=0, speed=100):
        self.x = x
        self.y = y
        self.vx = vx
        self.speed = speed