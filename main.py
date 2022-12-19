import machine, time
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY

DebugMode = False
pauseTime = 2

# Panel, 0 = Home, 1 = Work
Panel = 1

if DebugMode:
    time.sleep(pauseTime)

import msg
import fire
import supercomputer
import rainbow
import retroprompt

# overclock to 200Mhz
machine.freq(200000000)

# create galactic object and graphics surface for drawing
galactic = GalacticUnicorn()
graphics = PicoGraphics(DISPLAY)
effect = None

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

# Make Pen
def MakePen(grphcs,triple):
    pen = grphcs.create_pen(triple[0],triple[1],triple[2])

    return pen

# Send Debug Message To Display
def Msg(message):
    global pauseTime, COLOR_BLACK, COLOR_GRAY

    graphics.set_font("bitmap6")
    graphics.set_pen(MakePen(graphics,COLOR_BLACK))
    graphics.clear()
    graphics.set_pen(MakePen(graphics,COLOR_GRAY))
    graphics.text(message,0,-1,-1,1)
    print(message)
    galactic.update(graphics)
    time.sleep(pauseTime)

# Only print when in Debug Mode
def DbgMsg(message):
    global DebugMode

    if DebugMode:
        Msg(message)

# returns the id of the button that is currently pressed or
# None if none are
def pressed():
    if galactic.is_pressed(GalacticUnicorn.SWITCH_A):
        return GalacticUnicorn.SWITCH_A
    if galactic.is_pressed(GalacticUnicorn.SWITCH_B):
        return GalacticUnicorn.SWITCH_B
    if galactic.is_pressed(GalacticUnicorn.SWITCH_C):
        return GalacticUnicorn.SWITCH_C
    if galactic.is_pressed(GalacticUnicorn.SWITCH_D):
        return GalacticUnicorn.SWITCH_D
    return None

# Wait for Button Press
def WaitPressed():
    button = None

    while button == None:
        button = pressed()

        if button == None:
            time.sleep(0.001)

    return button

# Wait for Buttons Released
def WaitReleased():
    while pressed() != None:
        time.sleep(0.1)

# Send Notice to Display
def Notice():
    global graphics, COLOR_BLACK, COLOR_GRAY

    graphics.set_font("bitmap6")
    graphics.set_pen(MakePen(graphics,COLOR_BLACK))
    graphics.clear()
    graphics.set_pen(MakePen(graphics,COLOR_GRAY))
    graphics.text("PRESS", 12, -1, -1, 1)
    graphics.text("A B C OR D!", 2, 5, -1, 1)
    galactic.update(graphics)

    time.sleep(0.5)

#
# Button A Messages
#

# Message Data
# Color triple format is similar to btnC (Background,Text,Outline)
btnAMessages = None

if Panel == 0:
    btnAMessages = [
    ("Sheeboo is Out!", COLOR_RED, COLOR_WHITE, COLOR_BLACK),
    ("Sheeboo is In!", COLOR_GREEN, COLOR_WHITE, COLOR_BLACK),
    ("Eric is Out!", COLOR_PIMBLUE, COLOR_WHITE, COLOR_BLACK),
    ("Eric is In!", COLOR_GREEN, COLOR_WHITE, COLOR_BLACK),
    ("Cats have NOT been fed!",COLOR_RED,COLOR_WHITE,COLOR_BLACK),
    ("Cats HAVE been fed!",COLOR_GREEN,COLOR_WHITE,COLOR_BLACK),
    ("Cats have NOT been Crunchied!",COLOR_RED,COLOR_WHITE,COLOR_BLACK),
    ("Cats HAVE been Crunchied!",COLOR_GREEN,COLOR_WHITE,COLOR_BLACK)
    ]
elif Panel == 1:
    btnAMessages = [
    (">>> World Domination In Progress <<<", COLOR_RED, COLOR_WHITE, COLOR_BLACK),
    ("]]] Condition RED [[[", COLOR_RED, COLOR_WHITE, COLOR_BLACK),
    ("[[[ Condition Green ]]]", COLOR_GREEN, COLOR_WHITE, COLOR_BLACK),
    ("--> Go Away, You're Bothering Me <--", COLOR_PIMBLUE, COLOR_WHITE, COLOR_BLACK),
    ("Eric is In!", COLOR_GREEN, COLOR_WHITE, COLOR_BLACK),
    ("Eric is Out!", COLOR_PIMBLUE, COLOR_WHITE, COLOR_BLACK),
    (".xX No Stupid Zone In Effect Xx.", COLOR_GREEN, COLOR_WHITE, COLOR_BLACK),
    ("Leave Donations on the Desk, Cash or Hardware Only", COLOR_BLUE,COLOR_WHITE,COLOR_BLACK),
    ("I know nothing, I just work here...", COLOR_PURPLE, COLOR_WHITE,COLOR_BLACK),
    ]
else:
    btnAMessages = [
    ("Panel Test, Panel Test",COLOR_BLUE,COLOR_WHITE,COLOR_BLACK),
    ("Pllltththth!",COLOR_RED,COLOR_WHITE,COLOR_BLACK),
    ]

# Button A Current Message (tuple)
btnACurrentMsg = 0

#
# Button B Effects
#

# Current Effect for btnB
btnBCurrentEffect = 0

#
# Button C Messages
#

# btnC Message and Color data
# fmt: [ message, colors for circulation, current color, color1, ... ]
# If one color, then remaining colors are used for outline and foreground colors
# i.e. BACKGROUND, TEXT, OUTLINE
btnCMessages = [
    [ "Happy Halloween!", 1, 0, COLOR_SPOOKYGREEN, COLOR_RED, COLOR_BLACK ],
    [ "Happy Thanksgiving!", 1, 0, COLOR_ORANGE, COLOR_YELLOW, COLOR_BLACK ],
    [ "Merry Christmas!", 1, 0, COLOR_RED, COLOR_GREEN, COLOR_BLACK ],
    [ "Happy New Year!", 1,0, COLOR_WHITE, COLOR_GOLD, COLOR_BLACK ],
    [ "Happy Chinese New Year!", 1,0, COLOR_RED, COLOR_GOLD, COLOR_BLACK ],
    [ "Happy Easter!", 1, 0, COLOR_YELLOW, COLOR_BABYBLUE, COLOR_BLACK ],
    [ "Happy St. Patricks Day!", 1, 0, COLOR_GREEN, COLOR_WHITE, COLOR_BLACK ],
    [ "Happy Birthday!",1,0,COLOR_WHITE,COLOR_BLUE,COLOR_BLACK ],
    [ "Happy Birthday Sheila!",1,0,COLOR_WHITE,COLOR_RED,COLOR_BLACK ],
    [ "Happy Birthday Eric!",1,0,COLOR_WHITE,COLOR_GREEN,COLOR_BLACK ]
    ]

# Current btnC message
btnCCurrentMsg = 0

# Last Button Press
lastButtonPressed = None

# Display Initial Notice
Notice()

firecount = 0
supercomputercount = 0

fire.graphics = graphics
fire.set_palette(0)

# wait for a button to be pressed and load that effect
while True:
    time.sleep(0.1)

    try:
        while effect == None:
            if lastButtonPressed == None:
                lastButtonPressed = pressed()

            if lastButtonPressed == GalacticUnicorn.SWITCH_A:
                DbgMsg("In/Out")

                effect = msg

                data = btnAMessages[btnACurrentMsg]

                effect.SetMessage(data[0])
                effect.SetBackgroundColor(data[1])
                effect.SetMessageColor(data[2])
                effect.SetOutlineColor(data[3])

                btnACurrentMsg += 1
                btnACurrentMsg = (btnACurrentMsg % len(btnAMessages))
            elif lastButtonPressed == GalacticUnicorn.SWITCH_B:
                DbgMsg("Effects")

                if btnBCurrentEffect == 0:
                    effect = fire

                    effect.next_palette()
                    firecount += 1

                    if firecount >= len(effect.palettes):
                        btnBCurrentEffect += 1
                        firecount = 0
                elif btnBCurrentEffect == 1:
                    effect = supercomputer

                    effect.next_colour()
                    supercomputercount += 1

                    if supercomputercount >= len(effect.colours):
                        btnBCurrentEffect += 1
                        supercomputercount = 0
                elif btnBCurrentEffect == 2:
                    effect = rainbow
                    btnBCurrentEffect += 1
                else:
                    effect = retroprompt
                    btnBCurrentEffect += 1

                btnBCurrentEffect = (btnBCurrentEffect % 4)
            elif lastButtonPressed == GalacticUnicorn.SWITCH_C:
                DbgMsg("Holiday Msgs")

                effect = msg

                data = btnCMessages[btnCCurrentMsg]
                message = data[0]
                colorcount = data[1]
                currentcolor = data[2]
                color_triples = data[3:]

                effect.SetMessage(message)

                if colorcount == 1:
                    if len(color_triples) == 1:
                        print("Setting single color")
                        effect.SetBackgroundColor(color_triples[0])
                        effect.SetMessageColor(COLOR_PIMBLUE)
                    else:
                        print("Setting multi-color")
                        effect.SetBackgroundColor(color_triples[0])
                        effect.SetMessageColor(color_triples[1])
                        effect.SetOutlineColor(color_triples[2])
                else:
                    print("Shifting colors")
                    # Set next color and increment color index with modulo
                    effect.SetBackgroundColor(color_triples[currentcolor])
                    data[2] += 1
                    data[2] = (data[2] % len(color_triples))

                # Increment to next message with modulo
                btnCCurrentMsg += 1
                btnCCurrentMsg = (btnCCurrentMsg % len(btnCMessages))
            elif lastButtonPressed == GalacticUnicorn.SWITCH_D:
                DbgMsg("Halting")

                Msg("Halting...")

                break

            # wait until all buttons are released
            WaitReleased()

            lastButtonPressed = None
    except Exception as err:
        Msg(str(err))

    if effect != None:
        effect.graphics = graphics
        effect.init()

    brightness = 0.5
    sleep = False
    was_sleep_pressed = False

    # wait
    while effect != None:
        # if A, B, C, or D are pressed then reset

        lastButtonPressed = pressed()

        if lastButtonPressed != None:
            effect = None
            WaitReleased()
            break

        sleep_pressed = galactic.is_pressed(GalacticUnicorn.SWITCH_SLEEP)
        if sleep_pressed and not was_sleep_pressed:
            sleep = not sleep

        was_sleep_pressed = sleep_pressed

        if sleep:
            # fade out if screen not off
            galactic.set_brightness(galactic.get_brightness() - 0.05)

            if effect != None and galactic.get_brightness() > 0.0:
                effect.draw()

            # update the display
            galactic.update(graphics)

            if galactic.get_brightness() <= 0:
                time.sleep(0.09)
        elif effect != None:
            effect.draw()

            # update the display
            galactic.update(graphics)

            # brightness up/down
            if galactic.is_pressed(GalacticUnicorn.SWITCH_BRIGHTNESS_UP):
                brightness += 0.05
            if galactic.is_pressed(GalacticUnicorn.SWITCH_BRIGHTNESS_DOWN):
                brightness -= 0.05

            galactic.set_brightness(brightness)

        # pause for a moment (important or the USB serial device will fail
        time.sleep(0.01)

