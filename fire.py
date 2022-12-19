import time, random
from galactic import GalacticUnicorn

graphics = None
palette = None

palettes = []
currentPalette = -1

# setup heat value buffer and fire parameters
width = GalacticUnicorn.WIDTH + 2
height = GalacticUnicorn.HEIGHT + 4
heat = [[0.0 for y in range(height)] for x in range(width)]
fire_spawns = 5
damping_factor = 0.97

def create_palettes():
    global palettes, graphics
    
    if graphics != None:
        palette1 = [
        graphics.create_pen(  0,   0,   0),
        graphics.create_pen( 20,  20,  20),
        graphics.create_pen(180,  30,   0),
        graphics.create_pen(220, 160,   0),
        graphics.create_pen(255, 255, 180)
        ]
        palette2 = [
        graphics.create_pen(  0,   0,   0),
        graphics.create_pen( 20,  20,  20),
        graphics.create_pen(30,  180,   0),
        graphics.create_pen(160, 220,   0),
        graphics.create_pen(180, 255, 180)
        ]
        palette3 = [
        graphics.create_pen(  0,   0,   0),
        graphics.create_pen( 20,  20,  20),
        graphics.create_pen(30,  0,   180),
        graphics.create_pen(160, 0,   220),
        graphics.create_pen(180, 180, 255)
        ]
        
        palettes.append(palette1)
        palettes.append(palette2)
        palettes.append(palette3)
        
def set_palette(index):
    global palette,palettes
    
    if palettes == None or len(palettes) < 1:
        create_palettes()
    else:    
        index = (index % len(palettes))
    
        palette = palettes[index]
    
def next_palette():
    global currentPalette, palette, palettes
    
    if palettes == None or len(palettes) < 1:
        create_palettes()
    else:
        currentPalette += 1
        currentPalette = (currentPalette % len(palettes))
    
        palette = palettes[currentPalette]

def init():
    global palettes, palette
    # a palette of five firey colours (white, yellow, orange, red, smoke)

    if palettes == None or len(palettes) < 1:
        create_palettes()
    if palette == None:
        next_palette()
        
# returns the palette entry for a given heat value
@micropython.native  # noqa: F821
def pen_from_value(value):
    if value < 0.15:
        return palette[0]
    elif value < 0.25:
        return palette[1]
    elif value < 0.35:
        return palette[2]
    elif value < 0.45:
        return palette[3]
    return palette[4]

@micropython.native  # noqa: F821
def draw():
    global palette
    
    if palette == None:
        print("Palette is NONE")
        return
    
    # clear the the rows off the bottom of the display
    for x in range(width):
        heat[x][height - 1] = 0.0
        heat[x][height - 2] = 0.0
        
    # add new fire spawns
    for c in range(fire_spawns):
        x = random.randint(0, width - 4) + 2
        heat[x + 0][height - 1] = 1.0
        heat[x + 1][height - 1] = 1.0
        heat[x - 1][height - 1] = 1.0
        heat[x + 0][height - 2] = 1.0
        heat[x + 1][height - 2] = 1.0
        heat[x - 1][height - 2] = 1.0

    # average and damp out each value to create rising flame effect
    for y in range(0, height - 2):
        for x in range(1, width - 1):
            # update this pixel by averaging the below pixels
            average = (
                heat[x][y] + heat[x][y + 1] + heat[x][y + 2] + heat[x - 1][y + 1] + heat[x + 1][y + 1]
            ) / 5.0

            # damping factor to ensure flame tapers out towards the top of the displays
            average *= damping_factor

            # update the heat map with our newly averaged value
            heat[x][y] = average
           
    # render the heat values to the graphics buffer
    for y in range(GalacticUnicorn.HEIGHT):
        for x in range(GalacticUnicorn.WIDTH):
            graphics.set_pen(pen_from_value(heat[x + 1][y]))
            graphics.pixel(x, y)
            
def test():
    print("A")