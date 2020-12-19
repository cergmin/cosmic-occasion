from settings import *


class Player:
    def __init__(self, x, y, vx=0, vy=90, speed=200):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.speed = speed