import pygame, math, random
from particle import Particle
import numpy as np
import json

pygame.init()
pygame.mixer.init()
jump_sound = pygame.mixer.Sound("assets/sfx/jump.mp3")

# resolutions = [(1280, 720), (1366, 768), (1600, 900), (1920, 1080), (2560, 1440), (3840, 2160)]
#open resolutions from config json
# Load the JSON configuration file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

def update_values():
    global config
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    jump_sound.set_volume(0.5)

def update_resolution(width, height):
    global config
    config['resolution']['width'] = width
    config['resolution']['height'] = height
    update_config()
    update_values()

def update_config():
    global config
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)

# Access configuration values
WIDTH = config['resolution']['width']
HEIGHT = config['resolution']['height']
gravity = config['gravity'] / 1080 * HEIGHT
player_speed = config['player_speed'] * WIDTH / 1920
jump_height = config['jump_height'] * HEIGHT / 1080
time_scale = config['time_scale']
air_acceleration_factor = config['air_acceleration_factor'] * WIDTH / 1920
friction = config['friction'] * WIDTH / 1920
ground_friction = config['ground_friction'] * WIDTH / 1920
starting_level = config['starting_level']
hidden_objects_opacity = config['hidden_objects_opacity']
volume = config['volume']
FPS = config['fps']
fullscreen = config['fullscreen']
resolutions = config['AvailableResolutions']
jump_sound.set_volume(0.5*volume)
font = pygame.font.SysFont("Comic Sans MS", 36*WIDTH//1920)