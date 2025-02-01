from config import *
from player import Player
from platform import Platform
from levels import level1

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

# Initialize player and platforms
player = Player(640, 100)

platforms = level1.platforms

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    move_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
    move_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
    space_bar = keys[pygame.K_SPACE]

    screen.fill("black")

    player.update(dt, platforms, move_left, move_right, space_bar)
    player.draw(screen)

    for platform in platforms:
        platform.draw(screen)

    pygame.display.flip()

    # Limit FPS and calculate delta time
    dt = clock.tick(60/time_scale) / 1000 * time_scale

pygame.quit()
