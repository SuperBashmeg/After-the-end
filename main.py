# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
gravity = 9.8
acceleration = [0, 0]
velocity = [0, 0]

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    pygame.draw.circle(screen, "red", player_pos, 40)
    # Physics
    velocity[0] += acceleration[0] * dt
    velocity[1] += acceleration[1] * dt
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        acceleration[1] = -300
    if keys[pygame.K_s]:
        acceleration[1] = 300
    if keys[pygame.K_a]:
        acceleration[0] = -300
    if keys[pygame.K_d]:
        acceleration[0] = 300

    #gravity
    acceleration[1] += gravity

    player_pos.y += velocity[1] * dt
    player_pos.x += velocity[0] * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()