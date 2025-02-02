import math

from config import *
import pygame.gfxdraw

class Spike:
    def __init__(self, x, y, channels, width=20, height=50, color=pygame.Color(100, 100, 100), rotation=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.angle = math.pi+math.radians(rotation)  # Initial rotation angle
        self.channels = channels

    def draw(self, screen):

        # Draw the triangle
        points = []
        for i in range(3):
            angle = i * 2 * math.pi / 3 - math.pi / 2 + self.angle
            x = self.x + self.width * math.cos(angle)
            y = self.y - self.height * math.sin(angle)
            points.append((x, y))
        pygame.gfxdraw.aapolygon(screen, points, self.color)
        pygame.gfxdraw.filled_polygon(screen, points, self.color)
