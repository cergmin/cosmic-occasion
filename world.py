from settings import *


class World:
    def __init__(self, map):
        self.map = list(map)
        self.objects = set()

        for i, row in enumerate(self.map):
            for j, obj_char in enumerate(row):
                if obj_char == 'w':
                    self.objects.add(
                        Wall(
                            TILE_SIZE * j,
                            TILE_SIZE * i
                        )
                    )
                elif obj_char == '.':
                    pass
                else:
                    assert ValueError(
                        f"Object '{obj_char}' is undefined"
                    )


class WorldObject:
    def __init__(self, x, y, hight):
        self.x = x
        self.y = y
        self.hight = hight
    
    def get_info(self):
        return {
            'type': type(self).__name__,
            'x': self.x,
            'y': self.y,
            'height': self.hight
        }


class Wall(WorldObject):
    def __init__(self, x, y):
        super().__init__(x, y, 100)