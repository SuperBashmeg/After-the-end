from pygame import Vector2

from platform import *
from star import *
from spike import *
from config import font

with open('levels.json', 'r') as levels_file:
    levels = json.load(levels_file)

class Level:
    def __init__(self, platforms, spikes, star, start_position =pygame.Vector2(640, 100), texts = None):
        self.platforms = platforms
        self.star = star
        self.start_position = start_position
        self.spikes = spikes
        if texts is None:
            self.texts = []
        else:
            self.texts = texts

def update_level_to_resolutions(level):
    for platform in level.platforms:
        platform.x = platform.x/1920*WIDTH
        platform.y = platform.y/1080*HEIGHT
        platform.width = platform.width/1920*WIDTH
        platform.height = platform.height/1080*HEIGHT
    for spike in level.spikes:
        spike.x = spike.x/1920*WIDTH
        spike.y = spike.y/1080*HEIGHT
        spike.width = spike.width/1920*WIDTH
        spike.height = spike.height/1080*HEIGHT
    for text in level.texts:
        text[1] = (text[1][0]/1920*WIDTH, text[1][1]/1080*HEIGHT)
    level.star.x = level.star.x/1920*WIDTH
    level.star.y = level.star.y/1080*HEIGHT
    level.star.size = level.star.size/1920*WIDTH
    level.star.height = level.star.size/1080*HEIGHT
    level.star.width = level.star.size/1920*WIDTH
    level.start_position = Vector2(level.start_position.x/1920*WIDTH, level.start_position.y/1080*HEIGHT)

def return_level(level=1):
    level = convert_json_to_level("level"+str(level))
    update_level_to_resolutions(level)
    print(level.texts)
    return level


def convert_json_to_level(level_name):
    level = levels[level_name]
    platforms = []
    for platform in level['platforms']:
        platforms.append(Platform(platform['x'], platform['y'], platform['channels'], platform['width'], platform['height'], platform['color'], platform['collisions']['Left'], platform['collisions']['Bottom'], platform['collisions']['Right'], platform['collisions']['Top']))
    spikes = []
    for spike in level['spikes']:
        spikes.append(Spike(spike['x'], spike['y'], spike["channels"], spike['width'], spike['height'], spike['color'], spike['rotation']))
    star = Star(level['star']['x'], level['star']['y'], level['star']['size'])
    start_position = Vector2(level['player']['x'], level['player']['y'])
    texts = []
    for text in level['texts']:
        texts.append([font.render(text['text'], True, text['color']), (text['x'], text['y'])])
    return Level(platforms, spikes, star, start_position, texts)


# level0 = Level([
#     Platform(300, 500, [0, 1, 2], 400, 60),
#     Platform(740, 540, [0], 200, 60),
#     Platform(900, 400, [0], 200, 60),
#     Platform(440, 300, [1],10, 200, pygame.Color(0, 255, 0), True, True, True, True),
#     Platform(800, 300, [0],200, 25, pygame.Color(0, 255, 0), False, True, False, False),],
#     [Spike(640, 474, [1], 25, 50, [100, 100, 100])],
#     Star(200, 150),
#     pygame.Vector2(640, 100))
#
# level1 = Level([
#     Platform(0, 500, [0, 1, 2], 600, 50),
#     Platform(300, 300, [0], 25, 200),
# ] ,
#     [
#
#     ],
#     Star(500, 400),
#     pygame.Vector2(100, 100),
# [[font.render("To switch between time channels click [Q] and [E]", True, (200,200,0)), (100, 100)]]
# )

# level2 = Level([
#     Platform(0, 500, [0, 1, 2], 600, 50),
#     Platform(300, 300, [0], 25, 200),
# ] ,
#     [
#
#     ],
#     Star(500, 400),
#     pygame.Vector2(100, 100),
# [[font.render("To switch between time channels click [Q] and [E]", True, (200,200,0)), (100, 100)]]
# )