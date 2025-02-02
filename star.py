import random

import pygame
import math

from particle import Particle


class Star:
    def __init__(self, x, y, size=25, color=pygame.Color(255, 255, 0)):
        self.x = x
        self.y = y
        self.width = size
        self.height = size
        self.size = size
        self.color = color
        self.angle = 0  # Initial rotation angle
        self.trail = []  # List to store previous positions
        self.particles = []
        self.max_trail_length = 20  # Maximum length of the trail
        self.speed = 5  # Rotation speed
        self.particle_cooldown = 0.25  # Time between particle spawns

    def draw(self, screen):
        # Draw the trail

        for i, (x, y, angle) in enumerate(self.trail):
            alpha = int(50 * (i + 1) / len(self.trail))
            trail_color = (255, 255, 0, alpha)
            trail_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            trail_surface.fill((0, 0, 0, 0))
            points = []
            for j in range(10):
                trail_angle = j * math.pi / 5 - math.pi * 3 / 2 + angle
                radius = self.size if j % 2 == 0 else self.size / 2
                trail_x = self.size + radius * math.cos(trail_angle)
                trail_y = self.size - radius * math.sin(trail_angle)
                points.append((trail_x, trail_y))
            pygame.draw.polygon(trail_surface, trail_color, points)
            screen.blit(trail_surface, (x - self.size, y - self.size))

        for particle in self.particles:
            particle.draw(screen)
        # Draw the star
        points = []
        for i in range(10):
            angle = i * math.pi / 5 - math.pi * 3 / 2 + self.angle
            radius = self.size if i % 2 == 0 else self.size / 2
            x = self.x + radius * math.cos(angle)
            y = self.y - radius * math.sin(angle)
            points.append((x, y))
        pygame.draw.polygon(screen, self.color, points)

    def update(self, dt):
        self.angle += dt * self.speed * math.pi / 5  # Rotate the star continuously
        self.particle_cooldown -= dt
        for particle in self.particles:
            particle.update(dt)
            if particle.destroyed:
                self.particles.remove(particle)
        if self.particle_cooldown <= 0:
            self.particle_cooldown = 0.25
            size = random.randint(1, 10)
            self.particles.append(Particle((self.x, self.y), size, size, self.color, 1, [random.uniform(-50, 50), random.uniform(-50, 50)], random.uniform(0, 360), random.uniform(-10, 10), 0.5, 0.25))
        # Update the trail
        self.trail.append((self.x, self.y, self.angle))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)