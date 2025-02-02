import pygame

from config import *
from player import Player
from levels import return_level
from particle import Particle
from button import Button

# pygame setup
pygame.init()
pygame.display.set_caption("After The End Of Time")
pygame.display.set_icon(pygame.image.load("assets/icon.png"))
screen = pygame.display.set_mode([WIDTH, HEIGHT])

channels = [pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA) for _ in range(5)]
for channel in channels:
    channel.set_alpha(hidden_objects_opacity)

channels[0].set_alpha(255)
clock = pygame.time.Clock()
running = True
changing_channel = False
start_time = 0
target_channel = 0
dt = 0
font = pygame.font.SysFont("Comic Sans MS", 36)
text_color = (255, 255, 255)
text = font.render("Time: 1", True, text_color)
fps_text = font.render("FPS: 0", True, text_color)
is_main_menu = True
display_debug = False

particle_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
top_particle_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
particles = []
top_particles = []
levelId = starting_level
base_particle_respawn_time = 10
particle_respawn_time = 0
level = return_level(levelId)
star = level.star
player = Player(640, 100)
platforms = level.platforms
spikes = level.spikes

def spawn_background_particles(count):
    for _ in range(count):
        size = random.randint(5, 200)
        particles.append(Particle((random.randint(1, WIDTH), random.randint(1, HEIGHT)), size, size, (255, 255, 255, 10), 250, [random.uniform(-5, 5), random.uniform(-5, 5)], random.uniform(1, 360), random.uniform(-2, 2)))
spawn_background_particles(10)
def change_level(level, screen):
    global platforms, channels, player, levelId
    levelId += 1
    platforms = level.platforms
    channels = [pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA) for _ in range(3)]
    top_particles.append(Particle((WIDTH/2, 360), 1000, 1000, (125, 125, 0, 255), 0.5, [0, 0], 0, 0, 0.25, 0.5))
    for channel in channels:
        channel.set_alpha(hidden_objects_opacity)
    channels[0].set_alpha(255)
    player = Player(level.start_position.x, level.start_position.y)

def change_channel(channel):
    global channels, start_time, changing_channel, target_channel
    if channel < 0:
        channel = 2
    elif channel > 2:
        channel = 0

    player.channel = channel
    start_time = pygame.time.get_ticks()
    changing_channel = True
    target_channel = channel

    for i in range(3):
        if i == channel:
            channels[i].set_alpha(channels[i].get_alpha())
        else:
            channels[i].set_alpha(hidden_objects_opacity)

buttons = {
    "Start": Button(x=100, y=100, width=200, height=50, text="Start", font=font, color=(20, 20, 20), hover_color=(50, 50, 50),
           text_color=(255, 255, 255)),

}

def main_menu():
    global is_main_menu
    buttons["Start"].check_hover(pygame.mouse.get_pos())
    buttons["Start"].draw(screen)
    player.freeze = True
    if buttons["Start"].is_clicked(pygame.mouse.get_pos(), pygame.mouse.get_pressed()):
        is_main_menu = False
        player.freeze = False

def debug_info():
    global fps_text
    fps_text = font.render("FPS: " + str(int(clock.get_fps())), True, text_color)
    screen.blit(fps_text, (10, 50))

while running:
    screen.fill("black")
    particle_surface.fill("black")
    particle_respawn_time -= dt
    if particle_respawn_time <= 0:
        particle_respawn_time = base_particle_respawn_time
        size = random.randint(5, 200)
        spawn_background_particles(1)
        # particles.append(Particle((random.randint(1, WIDTH), random.randint(1, HEIGHT)), size, size, (255, 255, 255, 10), 50, [random.uniform(-5, 5), random.uniform(-5, 5)], random.uniform(1, 360), random.uniform(1, 5)))
    for particle in particles[:]:
        particle.update(dt)
        if particle.destroyed:
            particles.remove(particle)
        particle.draw(particle_surface)
    screen.blit(particle_surface, (0, 0))
    screen.blit(channels[0], (0, 0))
    screen.blit(channels[1], (0, 0))
    screen.blit(channels[2], (0, 0))
    star.draw(screen)
    if is_main_menu:
        main_menu()

    if display_debug:
        debug_info()

    if changing_channel:
        elapsed = pygame.time.get_ticks() - start_time
        duration = 500
        start_alpha = channels[target_channel].get_alpha()
        target_alpha = 255
        if elapsed < duration:
            alpha = start_alpha + (target_alpha - start_alpha) * (elapsed / duration)
            channels[target_channel].set_alpha(int(alpha))
        else:
            channels[target_channel].set_alpha(target_alpha)
            changing_channel = False

    text = font.render("Time Channel: " + str(player.channel), True, text_color)
    screen.blit(text, (10, 10))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                change_channel(player.channel + 1)
            elif event.key == pygame.K_q:
                change_channel(player.channel - 1)
            elif event.key == pygame.K_SPACE:
                player.jump_buffer = True
            elif event.key == pygame.K_1:
                change_channel(0)
            elif event.key == pygame.K_2:
                change_channel(1)
            elif event.key == pygame.K_3:
                change_channel(2)
            elif event.key == pygame.K_4:
                change_channel(3)
            elif event.key == pygame.K_5:
                change_channel(4)
            elif event.key == pygame.K_r:
                player.death()
            elif event.key == pygame.K_F3:
                display_debug = not display_debug
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                player.jump_buffer = False
                if player.velocity.y < 0:
                    player.velocity.y = 0
        elif event.type == pygame.USEREVENT + 1:
            change_channel(player.channel)

    keys = pygame.key.get_pressed()
    move_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
    move_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]


    if player.changing_level:
        change_level(return_level(levelId+1), screen)
        player.changing_level = False
    player.update(dt, level, move_left, move_right)
    player.draw(screen)
    star.update(dt)
    for platform in platforms:
        platform.update(dt)
        for channel in platform.channels:
            platform.draw(channels[channel])
    for spike in spikes:
        for channel in spike.channels:
            spike.draw(channels[channel])

    if len(top_particles) > 0:
        top_particle_surface.fill((0, 0, 0, 0))
        for particle in top_particles[:]:
            particle.update(dt)
            if particle.destroyed:
                top_particles.remove(particle)
            particle.draw(top_particle_surface)
        screen.blit(top_particle_surface, (0, 0))


    pygame.display.flip()
    # print(dt)
    # Limit FPS and calculate delta time
    dt = clock.tick(60/time_scale) / 1000 * time_scale

pygame.quit()
