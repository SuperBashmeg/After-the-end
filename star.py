from config import *

class Star:
    def __init__(self, x, y, size=25, color=pygame.Color(255, 255, 0)):
        self.x = x
        self.y = y
        self.size = size
        self.width = size
        self.height = size
        self.color = color
        self.angle = 0  # Initial rotation angle

    def draw(self, screen):
        scale_factor = 4
        large_surface = pygame.Surface((self.size * 2 * scale_factor, self.size * 2 * scale_factor), pygame.SRCALPHA)
        large_surface = large_surface.convert_alpha()
        large_surface.fill((0, 0, 0, 0))

        # Draw the star on the larger surface
        points = []
        for i in range(10):
            angle = i * math.pi / 5 - math.pi * 3 / 2 + self.angle
            radius = self.size * scale_factor if i % 2 == 0 else self.size * scale_factor / 2
            x = self.size * scale_factor + radius * math.cos(angle)
            y = self.size * scale_factor - radius * math.sin(angle)
            points.append((x, y))
        pygame.draw.polygon(large_surface, self.color, points)

        # Scale down the surface to the original size
        small_surface = pygame.transform.smoothscale(large_surface, (self.size * 2, self.size * 2))

        # Blit the small surface onto the screen
        screen.blit(small_surface, (self.x - self.size, self.y - self.size))

    def update(self, dt):
        self.angle += dt * 2 * math.pi / 5  # Rotate the star continuously