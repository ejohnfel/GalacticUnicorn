import time
from galactic import GalacticUnicorn

'''
Display scrolling wisdom, quotes or greetz.

You can adjust the brightness with LUX + and -.
'''

# Color Constants
COLOR_WHITE = (255,255,255)
COLOR_BLACK = (0,0,0)
COLOR_RED = (255,0,0)
COLOR_GREEN = (0,255,0)
COLOR_BLUE = (0,0,255)
COLOR_YELLOW = (255,255,0)
COLOR_ORANGE = (255,165,0)
COLOR_PURPLE = (128,0,128)
COLOR_PINK = (230,0,150)
COLOR_FUCHIA = (255,0,255)
COLOR_BABYBLUE = (204,255,255)
COLOR_GRAY = (155,155,155)
COLOR_BROWN = (153,102,51)
COLOR_PIMBLUE = (10,0,96)
COLOR_PIMORANGE = (230,150,0)
COLOR_SPOOKYGREEN = (102,255,153)
COLOR_TDAY = (128,128,0)

# constants for controlling scrolling text
PADDING = 4

MESSAGE_COLOUR = COLOR_WHITE
OUTLINE_COLOUR = COLOR_BLACK
BACKGROUND_COLOUR = COLOR_PIMBLUE

Messages = [ "Test Test" ]
CurrentMessage = -1
MESSAGE = None
HOLD_TIME = 2.0
STEP_TIME = 0.09

# state constants
STATE_PRE_SCROLL = 0
STATE_SCROLLING = 1
STATE_POST_SCROLL = 2

shift = 0
state = 0

# graphics object for surface for drawing
graphics = None

width = GalacticUnicorn.WIDTH
height = GalacticUnicorn.HEIGHT

last_time = time.ticks_ms()
time_ms = None

# function for drawing outlined text
def outline_text(text, x, y):
    global graphics, OUTLINE_COLOUR, MESSAGE_COLOUR
    
    graphics.set_pen(graphics.create_pen(int(OUTLINE_COLOUR[0]), int(OUTLINE_COLOUR[1]), int(OUTLINE_COLOUR[2])))
    graphics.text(text, x - 1, y - 1, -1, 1)
    graphics.text(text, x, y - 1, -1, 1)
    graphics.text(text, x + 1, y - 1, -1, 1)
    graphics.text(text, x - 1, y, -1, 1)
    graphics.text(text, x + 1, y, -1, 1)
    graphics.text(text, x - 1, y + 1, -1, 1)
    graphics.text(text, x, y + 1, -1, 1)
    graphics.text(text, x + 1, y + 1, -1, 1)

    graphics.set_pen(graphics.create_pen(int(MESSAGE_COLOUR[0]), int(MESSAGE_COLOUR[1]), int(MESSAGE_COLOUR[2])))
    graphics.text(text, x, y, -1, 1)

# Set Message
def SetMessage(message):
    global MESSAGE
    
    MESSAGE = message
    
def next_message():
    global MESSAGE, Messages, CurrentMessage
    
    CurrentMessage += 1
    CurrentMessage = (CurrentMessage % len(Messages))
    
    MESSAGE = Messages[CurrentMessage]

# Set Background Color
def SetBackgroundColor(background):
    global BACKGROUND_COLOUR
    
    BACKGROUND_COLOUR = background
    
# Set Outline Color
def SetOutlineColor(outline):
    global OUTLINE_COLOUR
    
    OUTLINE_COLOUR = outline

# Set Message Color
def SetMessageColor(msg_color):
    global MESSAGE_COLOUR
    
    MESSAGE_COLOUR = msg_color

# Init
def init():
    global graphics, MESSAGE

    # set the font
    graphics.set_font("bitmap8")
    
    if MESSAGE == None:
        next_message()

# Draw Function
@micropython.native
def draw():
    global graphics, last_time, time_ms, MESSAGE, HOLD_TIME, STATE_PRE_SCROLL, state, shift
    global BACKGROUND_COLOUR, PADDING
    
    # calculate the message width so scrolling can happen
    msg_width = graphics.measure_text(MESSAGE, 1)

    time_ms = time.ticks_ms()

    if state == STATE_PRE_SCROLL and time_ms - last_time > HOLD_TIME * 1000:
        if msg_width + PADDING * 2 >= width:
            state = STATE_SCROLLING
        last_time = time_ms

    if state == STATE_SCROLLING and time_ms - last_time > STEP_TIME * 1000:
        shift += 1
        if shift >= (msg_width + PADDING * 2) - width - 1:
            state = STATE_POST_SCROLL
        last_time = time_ms

    if state == STATE_POST_SCROLL and time_ms - last_time > HOLD_TIME * 1000:
        state = STATE_PRE_SCROLL
        shift = 0
        last_time = time_ms

    graphics.set_pen(graphics.create_pen(int(BACKGROUND_COLOUR[0]), int(BACKGROUND_COLOUR[1]), int(BACKGROUND_COLOUR[2])))
    graphics.clear()

    outline_text(MESSAGE, x=PADDING - shift, y=2)
