from config import *

class Platform:
    def __init__(self, x, y, channels, width=25, height=25, color=pygame.Color(255, 255, 255), left_collision=True, down_collision=True, right_collision=True, up_collision=True):
        if height < 25:
            height = 25
        if width < 50 and (not left_collision or not right_collision):
            width = 50
        self.type = "Static"
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.channels = channels
        self.collisions = {"left":left_collision,"down":down_collision,"right":right_collision, "up":up_collision}

    def update(self, dt):
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0, 2)


class MovingPlatform(Platform):
    def __init__(self, platform, end_x, end_y, period):

        super().__init__(platform.x, platform.y, platform.width, platform.height, platform.color, platform.collisions["left"], platform.collisions["down"], platform.collisions["right"], platform.collisions["up"])
        self.end_x = end_x
        self.end_y = end_y
        self.type = "Moving"
        self.period = period
        self.start_x = platform.x
        self.start_y = platform.y
        self.time_position = 0
        self.speed = pygame.Vector2((self.end_x - self.start_x) / (self.period/2), (self.end_y - self.start_y) / (self.period/2))


    def update(self, dt):
        if self.time_position >= self.period/2:
            self.time_position = -self.period/2

        if self.time_position > 0:
            self.speed = pygame.Vector2((self.end_x - self.start_x) / (self.period / 2),(self.end_y - self.start_y) / (self.period / 2))
        else:
            self.speed = pygame.Vector2((self.start_x - self.end_x) / (self.period / 2),(self.start_y - self.end_y) / (self.period / 2))

        self.x = self.start_x + abs(self.end_x * self.time_position / (self.period/2))
        self.y = self.start_y + abs(self.end_y * self.time_position / (self.period/2))

        self.time_position += dt