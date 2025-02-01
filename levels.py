from pygame import Vector2

from platform import *
from star import *

class Level:
    def __init__(self, platforms, star, start_position =pygame.Vector2(640, 100)):
        self.platforms = platforms
        self.star = star
        self.start_position = start_position

def return_level(level=1):
    if level == 1:
        return level1
    else:
        return level1

level1 = Level([
    Platform(300, 500, [0, 1, 2, 3, 4], 400, 60),
    Platform(740, 540, [0], 200, 60),
    Platform(900, 400, [0], 200, 60),
    Platform(440, 300, [1],10, 200, pygame.Color(0, 255, 0), True, True, True, True),
    Platform(800, 300, [0],200, 25, pygame.Color(0, 255, 0), False, True, False, False),],

    Star(200, 150), pygame.Vector2(640, 100))