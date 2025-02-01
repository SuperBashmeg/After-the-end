from config import *
from platform import Platform

class Level:
    def __init__(self, platforms):
        self.platforms = platforms


level1 = Level([
    Platform(300, 500, 400, 60),
    Platform(740, 540, 200, 60),
    Platform(900, 400, 150),
    Platform(440, 300, 50, 200, pygame.Color(0, 255, 0), False, True, True, True),
    Platform(800, 300, 200, 25, pygame.Color(0, 255, 0), False, True, False, False)
])