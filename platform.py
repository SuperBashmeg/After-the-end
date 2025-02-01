from config import *

class Platform:
    def __init__(self, x, y, width=25, height=25, color=pygame.Color(255, 255, 255), left_collision=True, down_collision=True, right_collision=True, up_collision=True):
        if height < 25:
            height = 25
        if width < 50 and (not left_collision or not right_collision):
            width = 50
        elif width < 25:
            width = 25
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.collisions = {"left":left_collision,"down":down_collision,"right":right_collision, "up":up_collision}

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))