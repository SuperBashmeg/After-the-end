import math

import pygame.transform

from config import *

# def spawn_particles(x, y, count, speed, rotation, size, color, mix_x, min_y, min_count, min_speed,
#                     min_rotation, min_size):
#     particles = []
#     for _ in range(count):
#         particle = Particle((x, y))
#         particle.velocity = [random.uniform(-speed, speed), random.uniform(-speed, speed)]
#         particle.rotation_speed = random.uniform(-rotation, rotation)
#         particle.radius = random.randint(size, size * 2)
#         particle.color = color
#         particles.append(particle)
#     return particles

# Particle class with rotation
class Particle:
    def __init__(self, position, width, height, color, lifetime, velocity, initial_rotation, rotation_speed, destroy_time=0.5, spawn_time=0.25):
        self.x, self.y = position
        self.width = 0
        self.base_width = width
        self.height = 0
        self.base_height = height
        self.color = color
        self.lifetime = lifetime
        self.velocity = velocity
        self.angle = initial_rotation  # Initial rotation angle
        self.rotation_speed = rotation_speed  # Degrees per frame
        self.destruction_time = destroy_time
        self.max_destruction_time = destroy_time
        self.destroyed = False
        self.spawning = True
        self.max_spawning = spawn_time
        self.spawn_time = spawn_time

    def update(self, dt):
        # Update position
        self.x += self.velocity[0]*dt
        self.y += self.velocity[1]*dt
        if not self.spawning:
            self.lifetime -= dt
        else:
            self.spawn(dt)
        if self.lifetime <= 0:
            self.destroy(dt)

        # Rotate the particle
        self.angle = (self.angle + self.rotation_speed*dt) % 360

    def spawn(self, dt):
        self.spawn_time -= dt
        if self.spawn_time <= 0:
            self.spawning = False
        self.width = self.base_width * math.cos(self.spawn_time* math.pi)
        self.height = self.base_height * math.cos(self.spawn_time* math.pi)

    def destroy(self, dt):
        self.destruction_time -= dt
        if self.destruction_time <= 0:
            self.destroyed = True
        self.width = self.base_width * math.sin(self.destruction_time*math.pi)
        self.height = self.base_height * math.sin(self.destruction_time*math.pi)

    def get_vertices(self):
        vertices = []
        for i in range(8):
            angle = 0
            if i % 2 == 0:
                angle = (i//2* math.pi /2-math.radians(2)) + math.radians(self.angle)
            else:
                angle = (i//2* math.pi /2+math.radians(2)) + math.radians(self.angle)



            x = self.x + self.width * math.cos(angle)
            y = self.y + self.height * math.sin(angle)
            vertices.append((x, y))
        return vertices


    def draw(self, surface):
        # pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), 0)
        pygame.draw.polygon(surface, self.color, self.get_vertices())