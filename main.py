import pygame

from config import *
from player import Player
from levels import level1

# pygame setup
pygame.init()
screen = pygame.display.set_mode([1280, 720])
channels = [pygame.Surface((1280, 720), pygame.SRCALPHA),pygame.Surface((1280, 720), pygame.SRCALPHA),pygame.Surface((1280, 720), pygame.SRCALPHA),pygame.Surface((1280, 720), pygame.SRCALPHA),pygame.Surface((1280, 720), pygame.SRCALPHA)]
clock = pygame.time.Clock()
running = True
dt = 0
font = pygame.font.SysFont("Comic Sans MS", 36)
text_color = (255, 255, 255)
text = font.render("Hello, Pygame!", True, text_color)

# Initialize player and platforms
player = Player(640, 100)

platforms = level1.platforms


while running:
    screen.fill("black")
    screen.blit(channels[0], (0, 0))
    screen.blit(channels[1], (0, 0))
    screen.blit(channels[2], (0, 0))
    screen.blit(channels[3], (0, 0))
    screen.blit(channels[4], (0, 0))
    text = font.render("Current Channel: " + str(player.channel), True, text_color)
    screen.blit(text, (10, 10))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                channels[player.channel].set_alpha(120)
                player.channel += 1
                if player.channel > 4:
                    player.channel = 0
                channels[player.channel].set_alpha(255)
            elif event.key == pygame.K_q:
                channels[player.channel].set_alpha(120)
                player.channel -= 1
                if player.channel < 0:
                    player.channel = 4
                channels[player.channel].set_alpha(255)

    keys = pygame.key.get_pressed()
    move_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
    move_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
    space_bar = keys[pygame.K_SPACE]



    player.update(dt, platforms, move_left, move_right, space_bar)
    player.draw(screen)
    for platform in platforms:
        platform.update(dt)
        for channel in platform.channels:
            platform.draw(channels[channel])


    pygame.display.flip()

    # Limit FPS and calculate delta time
    dt = clock.tick(60/time_scale) / 1000 * time_scale

pygame.quit()
