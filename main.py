import pygame.display

from config import *
from player import Player
from levels import return_level
from particle import Particle
from button import Button

print(resolutions)

def check_resolution_available(width, height):
    for resolution in resolutions:
        if resolution['width'] == width and resolution['height'] == height:
            print("Resolution available")
            return True
    return False

def get_resolution_index(width, height):
    for i, resolution in enumerate(resolutions):
        if resolution['width'] == width and resolution['height'] == height:
            return i
    return -1

# pygame setup
pygame.display.set_caption("After The End Of Time")
pygame.display.set_icon(pygame.image.load("assets/icon.png"))
max_width = pygame.display.Info().current_w
max_height = pygame.display.Info().current_h

if not check_resolution_available(WIDTH, HEIGHT):
    resolutions.append({"width": WIDTH, "height": HEIGHT})
    update_config()
if not WIDTH or not HEIGHT:
    WIDTH, HEIGHT = max_width, max_height
    config['resolution']['width'] = WIDTH
    config['resolution']['height'] = HEIGHT
    update_config()
    update_values()
    if not check_resolution_available(WIDTH, HEIGHT):
        resolutions.append({"width": WIDTH, "height": HEIGHT})
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.FULLSCREEN if fullscreen else 0)



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
text_color = (255, 255, 255)
text = font.render("", True, text_color)
# fps_text = font.render("FPS: 0", True, text_color)
is_main_menu = True
is_options = False
is_credit = False
is_escape = False
display_debug = False
channel_change_allowed = True

black_tint = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
black_tint.fill((0, 0, 0, 200))
particle_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
top_particle_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
level_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
particles = []
top_particles = []
levelId = starting_level
base_particle_respawn_time = 10
particle_respawn_time = 0
level = return_level(0)
star = level.star
player = Player(640, 100, 50/1920*WIDTH, 50/1080*HEIGHT)
platforms = level.platforms
spikes = level.spikes
texts = level.texts
to_close = False

def spawn_background_particles(count):
    for _ in range(count):
        size = random.randint(5, 200)
        particles.append(Particle((random.randint(1, WIDTH), random.randint(1, HEIGHT)), size, size, (255, 255, 255, 10), 250, [random.uniform(-5, 5), random.uniform(-5, 5)], random.uniform(1, 360), random.uniform(-2, 2)))
spawn_background_particles(10)
def change_level(new_id, color=(150, 125, 0, 255)):
    global platforms, channels, player, spikes, star, level, texts
    level = return_level(new_id)
    platforms = level.platforms
    spikes = level.spikes
    star = level.star
    texts = level.texts
    channels = [pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA) for _ in range(3)]
    size = HEIGHT*1.5
    top_particles.append(Particle((WIDTH/2, HEIGHT/2), size, size , color, 0.5, [0, 0], 0, 360, 0.25, 0.5))
    for channel in channels:
        channel.set_alpha(hidden_objects_opacity)
    channels[0].set_alpha(255)
    player = Player(level.start_position.x, level.start_position.y, 50/1920*WIDTH, 50/1080*HEIGHT)
    draw_level()

def change_channel(channel):
    global channels, start_time, changing_channel, target_channel
    if not channel_change_allowed:
        return
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




ui_elements = {
    "Title": pygame.font.SysFont("Comic Sans MS", 64).render("After The End Of Time", True, text_color),
    "Start": Button(x=WIDTH/2-WIDTH*0.125, y=HEIGHT*0.236, width=WIDTH*0.25, height=HEIGHT*0.07, text="Start", font=font, color=(20, 20, 20), hover_color=(50, 50, 50),
           text_color=(255, 255, 255)),
    "Options": Button(x=WIDTH/2-WIDTH*0.1, y=HEIGHT*0.39, width=WIDTH*0.2, height=HEIGHT*0.07, text="Options", font=font, color=(20, 20, 20), hover_color=(50, 50, 50),
           text_color=(255, 255, 255)),
    "Credits_button": Button(x=WIDTH/2-WIDTH*0.075, y=HEIGHT*0.54, width=WIDTH*0.15, height=HEIGHT*0.07, text="Credits", font=font, color=(10, 10, 10), hover_color=(10, 10, 10),
              text_color=(125, 125, 125)),
    "Quit": Button(x=WIDTH/2-WIDTH*0.05, y=HEIGHT*0.7, width=WIDTH*0.1, height=HEIGHT*0.07, text="Quit", font=font, color=(20, 20, 20), hover_color=(50, 50, 50),
                   text_color=(255, 255, 255)),
    "Resume": Button(x=WIDTH/2-WIDTH*0.125, y=HEIGHT*0.236, width=WIDTH*0.25, height=HEIGHT*0.07, text="Resume", font=font, color=(20, 20, 20), hover_color=(50, 50, 50),
                     text_color=(255, 255, 255)),
    "Main Menu": Button(x=WIDTH/2-WIDTH*0.075, y=HEIGHT*0.54, width=WIDTH*0.15, height=HEIGHT*0.07, text="Main Menu", font=font, color=(20, 20, 20), hover_color=(50, 50, 50),
                text_color=(255, 255, 255)),
}

options_ui = {
    "Title": pygame.font.SysFont("Comic Sans MS", 64).render("Options", True, text_color),
    "Back": Button(x=WIDTH*0.075, y=HEIGHT*0.5, width=WIDTH*0.4, height=HEIGHT*0.07, text="Back", font=font, color=(20, 20, 20), hover_color=(50, 50, 50),
                   text_color=(255, 255, 255)),
    "Volume": Button(x=WIDTH*0.075, y=HEIGHT*0.3, width=WIDTH*0.4, height=HEIGHT*0.07, text="Volume: 100%", font=font, color=(20, 20, 20), hover_color=(50, 50, 50),
                     text_color=(255, 255, 255)),
    "Trail Length": Button(x=WIDTH*0.525, y=HEIGHT*0.3, width=WIDTH*0.4, height=HEIGHT*0.07, text="Trail Length: 20", font=font, color=(20, 20, 20), hover_color=(50, 50, 50),
                        text_color=(255, 255, 255)),
    "Resolution": Button(x=WIDTH*0.075, y=HEIGHT*0.2, width=WIDTH*0.4, height=HEIGHT*0.07, text="Resolution: " + str(WIDTH) + "x" + str(HEIGHT), font=font, color=(20, 20, 20), hover_color=(50, 50, 50),
                        text_color=(255, 255, 255)),
    "Fullscreen": Button(x=WIDTH*0.525, y=HEIGHT*0.2, width=WIDTH*0.4, height=HEIGHT*0.07, text="Fullscreen: " + ("On" if fullscreen else "Off"), font=font, color=(20, 20, 20), hover_color=(50, 50, 50),
                        text_color=(255, 255, 255)),
    "Confirm": Button(x=WIDTH*0.525, y=HEIGHT*0.5, width=WIDTH*0.4, height=HEIGHT*0.07, text="Confirm", font=font, color=(20, 20, 20), hover_color=(50, 50, 50),
                     text_color=(255, 255, 255)),
}

restart = {
    "Title": pygame.font.SysFont("Comic Sans MS", 64).render("Please Restart The Game", True, (200, 0, 0)),
    "Restart": Button(x=WIDTH/2-WIDTH*0.25, y=HEIGHT*0.236, width=WIDTH*0.5, height=HEIGHT*0.07, text="Close The Game", font=font, color=(20, 20, 20), hover_color=(50, 50, 50),
              text_color=(200, 0, 0)),
}

def is_channel_empty(channel):
    pixel_array = pygame.surfarray.pixels_alpha(channel)
    return np.all(pixel_array == 0)

def escape_menu():
    global is_escape, is_main_menu, channel_change_allowed, is_options
    if is_options:
        options_menu()
        return
    player.freeze = True
    screen.blit(black_tint, (0, 0))
    screen.blit(ui_elements["Title"], (WIDTH/2 - ui_elements["Title"].get_width()/2, 20))
    ui_elements["Resume"].check_hover(pygame.mouse.get_pos())
    ui_elements["Resume"].update(dt)
    ui_elements["Resume"].draw(screen)
    ui_elements["Options"].check_hover(pygame.mouse.get_pos())
    ui_elements["Options"].update(dt)
    ui_elements["Options"].draw(screen)
    ui_elements["Main Menu"].check_hover(pygame.mouse.get_pos())
    ui_elements["Main Menu"].update(dt)
    ui_elements["Main Menu"].draw(screen)

    if ui_elements["Resume"].is_clicked(pygame.mouse.get_pos(), pygame.mouse.get_pressed()):
        is_escape = False
        player.freeze = False
        channel_change_allowed = True
    elif ui_elements["Options"].is_clicked(pygame.mouse.get_pos(), pygame.mouse.get_pressed()):
        is_options = True
    elif ui_elements["Main Menu"].is_clicked(pygame.mouse.get_pos(), pygame.mouse.get_pressed()):
        is_main_menu = True
        is_escape = False
        player.freeze = True
        player.draw_player = False
        channel_change_allowed = True
        change_level(0, (15, 15, 15, 255))

changes = {}
resolution_index, total_resolutions = get_resolution_index(WIDTH, HEIGHT), len(resolutions)
def close():
    global to_close, restart, screen, running
    to_close = True
    screen.blit(black_tint, (0, 0))
    screen.blit(restart["Title"], (0, 20))
    restart["Restart"].check_hover(pygame.mouse.get_pos())
    restart["Restart"].update(dt)
    restart["Restart"].draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if restart["Restart"].is_clicked(pygame.mouse.get_pos(), pygame.mouse.get_pressed()):
                running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

def options_menu():

    global is_options, screen, fullscreen, running, changes, resolution_index, total_resolutions, WIDTH, HEIGHT, to_close
    if to_close:
        close()
        return
    screen.blit(black_tint, (0, 0))
    screen.blit(options_ui["Title"], (WIDTH/2 - options_ui["Title"].get_width()/2, 20))
    options_ui["Back"].check_hover(pygame.mouse.get_pos())
    options_ui["Back"].update(dt)
    options_ui["Back"].draw(screen)
    options_ui["Volume"].check_hover(pygame.mouse.get_pos())
    options_ui["Volume"].update(dt)
    options_ui["Volume"].draw(screen)
    options_ui["Trail Length"].check_hover(pygame.mouse.get_pos())
    options_ui["Trail Length"].update(dt)
    options_ui["Trail Length"].draw(screen)
    options_ui["Resolution"].check_hover(pygame.mouse.get_pos())
    options_ui["Resolution"].update(dt)
    options_ui["Resolution"].draw(screen)
    options_ui["Fullscreen"].check_hover(pygame.mouse.get_pos())
    options_ui["Fullscreen"].update(dt)
    options_ui["Fullscreen"].draw(screen)
    options_ui["Confirm"].check_hover(pygame.mouse.get_pos())
    options_ui["Confirm"].update(dt)
    options_ui["Confirm"].draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if options_ui["Back"].is_clicked(pygame.mouse.get_pos(), pygame.mouse.get_pressed()):
                is_options = False
            elif options_ui["Volume"].is_clicked(pygame.mouse.get_pos(), pygame.mouse.get_pressed()):
                pass
            elif options_ui["Trail Length"].is_clicked(pygame.mouse.get_pos(), pygame.mouse.get_pressed()):
                pass
            elif options_ui["Resolution"].is_clicked(pygame.mouse.get_pos(), pygame.mouse.get_pressed()):
                resolution_index += 1
                if resolution_index >= total_resolutions:
                    resolution_index = 0
                while resolutions[resolution_index]['width'] > max_width or resolutions[resolution_index]['height'] > max_height:
                    resolution_index += 1
                    if resolution_index >= total_resolutions:
                        resolution_index = 0

                resolution = resolutions[resolution_index]
                options_ui["Resolution"].text = "Resolution: " + str(resolution['width']) + "x" + str(resolution['height'])
                changes["resolution"] = resolution
            elif options_ui["Fullscreen"].is_clicked(pygame.mouse.get_pos(), pygame.mouse.get_pressed()):
                options_ui["Fullscreen"].text = "Fullscreen: " + ("Off" if fullscreen else "On")
                changes["fullscreen"] = not fullscreen
                fullscreen = not fullscreen
            elif options_ui["Confirm"].is_clicked(pygame.mouse.get_pos(), pygame.mouse.get_pressed()):
                for change in changes:
                    config[change] = changes[change]
                is_options = False
                if "fullscreen" in changes:
                    pass
                if "resolution" in changes:
                    WIDTH = changes["resolution"]["width"]
                    HEIGHT = changes["resolution"]["height"]
                    to_close = True
                    is_options = True
                if changes:
                    screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.FULLSCREEN if fullscreen else 0)
                    update_config()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_options = False
                changes = {}



def main_menu():
    global is_main_menu, running, is_options
    if is_options:
        options_menu()
        return
    player.draw_player = False
    ui_elements["Start"].check_hover(pygame.mouse.get_pos())
    ui_elements["Start"].update(dt)
    ui_elements["Start"].draw(screen)
    ui_elements["Options"].check_hover(pygame.mouse.get_pos())
    ui_elements["Options"].update(dt)
    ui_elements["Options"].draw(screen)
    ui_elements["Credits_button"].check_hover(pygame.mouse.get_pos())
    # ui_elements["Credits_button"].update(dt)
    ui_elements["Credits_button"].draw(screen)
    ui_elements["Quit"].check_hover(pygame.mouse.get_pos())
    ui_elements["Quit"].update(dt)
    ui_elements["Quit"].draw(screen)
    screen.blit(ui_elements["Title"], (WIDTH/2 - ui_elements["Title"].get_width()/2, 20))
    player.freeze = True
    if ui_elements["Start"].is_clicked(pygame.mouse.get_pos(), pygame.mouse.get_pressed()):
        change_level(starting_level, (15, 15, 15, 255))
        is_main_menu = False
        player.freeze = False
        player.draw_player = True
    elif ui_elements["Options"].is_clicked(pygame.mouse.get_pos(), pygame.mouse.get_pressed()):
        is_options = True
    elif ui_elements["Credits_button"].is_clicked(pygame.mouse.get_pos(), pygame.mouse.get_pressed()):
        pass
    elif ui_elements["Quit"].is_clicked(pygame.mouse.get_pos(), pygame.mouse.get_pressed()):
        running = False

peak_positive_velocity_x = 0
peak_negative_velocity_x = 0
peak_positive_velocity_y = 0
peak_negative_velocity_y = 0
peak_velocity_timer = 0
def debug_info():
    global peak_positive_velocity_x, peak_negative_velocity_x, peak_positive_velocity_y, peak_negative_velocity_y, peak_velocity_timer
    if player.velocity.x > peak_positive_velocity_x:
        peak_positive_velocity_x = player.velocity.x
        peak_velocity_timer = 5
    if player.velocity.x < peak_negative_velocity_x:
        peak_negative_velocity_x = player.velocity.x
        peak_velocity_timer = 5
    if player.velocity.y > peak_positive_velocity_y:
        peak_positive_velocity_y = player.velocity.y
        peak_velocity_timer = 5
    if player.velocity.y < peak_negative_velocity_y:
        peak_negative_velocity_y = player.velocity.y
        peak_velocity_timer = 5
    if peak_velocity_timer > 0:
        peak_velocity_timer -= dt
    else:
        peak_positive_velocity_x = 0
        peak_negative_velocity_x = 0
        peak_positive_velocity_y = 0
        peak_negative_velocity_y = 0

    fps_text = font.render("FPS: " + str(int(clock.get_fps())), True, text_color)
    coyote_time_text = font.render("Coyote Timer: " + str(round(player.coyote_timer, 3)), True, text_color)
    on_ground_text = font.render("On Ground: " + str(player.on_ground), True, text_color)
    velocity_text = font.render("Velocity: " + str(player.velocity) + str([peak_positive_velocity_x, peak_positive_velocity_y]) + str([peak_negative_velocity_x, peak_negative_velocity_y]), True, text_color)
    acceleration_text = font.render("Acceleration: " + str(player.acceleration), True, text_color)
    position_text = font.render("Position: " + str([player.x, player.y]), True, text_color)
    collisions = player.get_collisions(level)
    display_collisions = []

    for collision in collisions:
        if len(collisions[collision]) > 0:
            display_collisions.append(collision)

    collisions_text = font.render("Collisions: " + str(display_collisions), True, text_color)


    screen.blit(fps_text, (10, 50))
    screen.blit(coyote_time_text, (10, 100))
    screen.blit(on_ground_text, (10, 150))
    screen.blit(collisions_text, (10, 200))
    screen.blit(velocity_text, (10, 250))
    screen.blit(acceleration_text, (10, 300))
    screen.blit(position_text, (10, 350))

def draw_level():
    level_surface.fill((0, 0, 0, 0))
    level_surface.blit(channels[0], (0, 0))
    level_surface.blit(channels[1], (0, 0))
    level_surface.blit(channels[2], (0, 0))


while running:
    if is_channel_empty(level_surface):
        print("Redraw")
        draw_level()
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
    star.draw(screen)
    screen.blit(level_surface, (0, 0))
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
        draw_level()

    if not is_main_menu:
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
            elif event.key == pygame.K_r:
                player.death()
            elif event.key == pygame.K_F3:
                display_debug = not display_debug
            elif event.key == pygame.K_ESCAPE:
                if not is_main_menu:
                    is_escape = not is_escape
                    player.freeze = is_escape
                    channel_change_allowed = not is_escape
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
        change_level(levelId+1)
        levelId+=1
        player.changing_level = False
    player.update(dt, level, move_left, move_right)
    player.draw(screen)
    star.update(dt)
    for platform in platforms:
        # platform.update(dt)
        for channel in platform.channels:
            platform.draw(channels[channel])
    for spike in spikes:
        for channel in spike.channels:
            spike.draw(channels[channel])

    for text in texts:
        screen.blit(text[0], text[1])

    if len(top_particles) > 0:
        top_particle_surface.fill((0, 0, 0, 0))
        for particle in top_particles[:]:
            particle.update(dt)
            if particle.destroyed:
                top_particles.remove(particle)
            particle.draw(top_particle_surface)
        screen.blit(top_particle_surface, (0, 0))

    if is_escape:
        escape_menu()

    pygame.display.flip()
    # print(dt)
    # Limit FPS and calculate delta time
    dt = clock.tick(FPS/time_scale) / 1000 * time_scale

pygame.quit()
