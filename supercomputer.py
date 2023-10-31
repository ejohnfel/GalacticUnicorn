import time, random
from galactic import GalacticUnicorn

graphics = None

# Color Constants
COLOR_WHITE = (255,255,255)
COLOR_BLACK = (0,0,0)
COLOR_RED = (255,0,0)
COLOR_GREEN = (0,255,0)
COLOR_BLUE = (0,0,255)
COLOR_YELLOW = (255,255,0)
COLOR_GOLD = (255,215,0)
COLOR_ORANGE = (255,165,0)
COLOR_PURPLE = (128,0,128)
COLOR_PINK = (230,0,150)
COLOR_REDPINK = (255,0,200)
COLOR_FUCHIA = (255,0,255)
COLOR_BABYBLUE = (51,102,255)
COLOR_GRAY = (155,155,155)
COLOR_BROWN = (153,102,51)
COLOR_PIMBLUE = (10,0,96)
COLOR_PIMORANGE = (230,150,0)
COLOR_SPOOKYGREEN = (102,255,153)
COLOR_TDAY = (128,128,0)

random_colors = [
    COLOR_WHITE,
    COLOR_RED,
    COLOR_GREEN,
    COLOR_BLUE,
    COLOR_YELLOW,
    COLOR_GOLD,
    COLOR_ORANGE,
    COLOR_PURPLE,
    COLOR_PINK,
    COLOR_REDPINK,
    COLOR_FUCHIA,
    COLOR_BABYBLUE,
    COLOR_GRAY,
    COLOR_BROWN,
    COLOR_PIMBLUE,
    COLOR_PIMORANGE,
    COLOR_SPOOKYGREEN,
    COLOR_TDAY    
    ]

colours = [ COLOR_PIMORANGE, COLOR_RED, COLOR_GREEN, COLOR_BLUE, COLOR_PINK, COLOR_PURPLE, COLOR_BROWN ]
colourIndex = -1
colour = None

use_random_colors = False
random_pixels = None

def random_color():
    index = random.randrange(0,len(random_colors) -1)
    
    return random_colors[index]

def next_colour():
    global colour, colours, colourIndex
    
    colourIndex += 1
    colourIndex = (colourIndex % len(colours))
    colour = colours[colourIndex]

def init():
    global width, height, lifetime, age, colour, random_pixels
    
    width = GalacticUnicorn.WIDTH
    height = GalacticUnicorn.HEIGHT
    
    if colour == None:
        next_colour()
    
    lifetime = [[0.0 for y in range(height)] for x in range(width)]
    age = [[0.0 for y in range(height)] for x in range(width)]
    random_pixels = [[random_color() for y in range(height)] for x in range(width)]
    
    for y in range(height):
        for x in range(width):
            lifetime[x][y] = 1.0 + random.uniform(0.0, 0.1)
            age[x][y] = random.uniform(0.0, 1.0) * lifetime[x][y]
            
@micropython.native  # noqa: F821
def draw():
    for y in range(height):
        for x in range(width):
            if age[x][y] >= lifetime[x][y]:
                age[x][y] = 0.0
                lifetime[x][y] = 1.0 + random.uniform(0.0, 0.1)

            age[x][y] += 0.025
            
    for y in range(height):
        for x in range(width):
            if use_random_colors:
                current_colour = random_pixels[x][y]
            else:
                current_colour = colour
                
            if age[x][y] < lifetime[x][y] * 0.3:
                graphics.set_pen(graphics.create_pen(current_colour[0], current_colour[1], current_colour[2]))
            elif age[x][y] < lifetime[x][y] * 0.5:
                decay = (lifetime[x][y] * 0.5 - age[x][y]) * 5.0
                graphics.set_pen(graphics.create_pen(int(decay * current_colour[0]), int(decay * current_colour[1]), int(decay * current_colour[2])))
            else:
                if use_random_colors:
                    random_pixels[x][y] = random_color()

                graphics.set_pen(0)
                
            graphics.pixel(x, y)