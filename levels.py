from config import *
from platform import *

class Level:
    def __init__(self, platforms):
        self.platforms = platforms

level1 = Level([
    Platform(300, 500, [0, 1, 2, 3, 4], 400, 60),
    Platform(740, 540, [0], 200, 60),
    Platform(900, 400, [0], 200, 60),
    Platform(440, 300, [1],50, 200, pygame.Color(0, 255, 0), True, True, True, True),
    Platform(800, 300, [0],200, 25, pygame.Color(0, 255, 0), False, True, False, False),
])