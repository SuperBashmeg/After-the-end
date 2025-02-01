import pygame

from config import *
from player import Player
from levels import return_level

# pygame setup
pygame.init()
pygame.display.set_caption("After The End Of Time")
pygame.display.set_icon(pygame.image.load("assets/icon.png"))
screen = pygame.display.set_mode([1280, 720])
channels = [pygame.Surface((1280, 720), pygame.SRCALPHA) for _ in range(5)]
for channel in channels:
    channel.set_alpha(120)

channels[0].set_alpha(255)
clock = pygame.time.Clock()
running = True
dt = 0
font = pygame.font.SysFont("Comic Sans MS", 36)
text_color = (255, 255, 255)
text = font.render("Time: 1", True, text_color)

levelId = starting_level
level = return_level(levelId)
star = level.star
# Initialize player and platforms
player = Player(640, 100)
platforms = level.platforms

#Change level
#platforms = level2.platforms
#channels = [pygame.Surface((1280, 720), pygame.SRCALPHA) for _ in range(5)]

def change_level(level):
    global platforms, channels, player, levelId
    levelId += 1
    platforms = level.platforms
    channels = [pygame.Surface((1280, 720), pygame.SRCALPHA) for _ in range(5)]
    for channel in channels:
        channel.set_alpha(120)
    channels[0].set_alpha(255)
    player = Player(level.start_position.x, level.start_position.y)

while running:
    screen.fill("black")
    screen.blit(channels[0], (0, 0))
    screen.blit(channels[1], (0, 0))
    screen.blit(channels[2], (0, 0))
    screen.blit(channels[3], (0, 0))
    screen.blit(channels[4], (0, 0))
    star.draw(screen)

    text = font.render("Time Channel: " + str(player.channel), True, text_color)
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
            elif event.key == pygame.K_SPACE:
                player.jump_buffer = True
            elif event.key == pygame.K_1:
                channels[player.channel].set_alpha(120)
                player.channel = 0
                channels[player.channel].set_alpha(255)
            elif event.key == pygame.K_2:
                channels[player.channel].set_alpha(120)
                player.channel = 1
                channels[player.channel].set_alpha(255)
            elif event.key == pygame.K_3:
                channels[player.channel].set_alpha(120)
                player.channel = 2
                channels[player.channel].set_alpha(255)
            elif event.key == pygame.K_4:
                channels[player.channel].set_alpha(120)
                player.channel = 3
                channels[player.channel].set_alpha(255)
            elif event.key == pygame.K_5:
                channels[player.channel].set_alpha(120)
                player.channel = 4
                channels[player.channel].set_alpha(255)



        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                player.jump_buffer = False
                if player.velocity.y < 0:
                    player.velocity.y = 0

    keys = pygame.key.get_pressed()
    move_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
    move_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
    space_bar = keys[pygame.K_SPACE]


    if player.changing_level:
        change_level(return_level(levelId+1))
        player.changing_level = False
    player.update(dt, level, move_left, move_right)
    player.draw(screen)
    star.update(dt)
    for platform in platforms:
        platform.update(dt)
        for channel in platform.channels:
            platform.draw(channels[channel])


    pygame.display.flip()

    # Limit FPS and calculate delta time
    dt = clock.tick(60/time_scale) / 1000 * time_scale

pygame.quit()
