import time
import board
import neopixel
import adafruit_fancyled.adafruit_fancyled as fancy
import random


# On CircuitPlayground Express, and boards with built in status NeoPixel -> board.NEOPIXEL
# Otherwise choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D1
pixel_pin = board.D0

# On a Raspberry pi, use this instead, not all pins are supported
# pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 64

# master brightness 0 to 1
brightness = 0.3

# number of x, y, z layers
size_x = 4
size_y = 4
size_z = 4

hue = 0

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=1.0, auto_write=False, pixel_order=ORDER
)


# return LED number for x,y,z coordinate
def XYZ(x, y, z):
    if z % 2:  # odd z-layers run forwards
        if x % 2:  # odd y-columns run backwards
            i = (x * 4) + (3 - y) + (z * 16)
        else:
            i = (x * 4) + y + (z * 16)
    else:  # even z-layers run backwards
        if x % 2:  # odd y-columns run forwards
            i = (3 - x) * 4 + y + (z * 16)
        else:
            i = (3 - x) * 4 + (3 - y) + (z * 16)

    return i


def updown():
    global hue
    wait = 0.1
    for z in range(4):
        for x in range(4):
            for y in range(4):
                i = XYZ(x, y, z)
                color = fancy.CHSV(hue % 255)
                color = fancy.gamma_adjust(color, brightness=brightness)
                pixels[i] = color.pack()
                hue += 1
        pixels.show()
        time.sleep(wait)


def leftright():
    global hue
    wait = 0.1
    for x in range(4):
        for y in range(4):
            for z in range(4):
                i = XYZ(x, y, z)
                color = fancy.CHSV(hue % 255)
                color = fancy.gamma_adjust(color, brightness=brightness)
                pixels[i] = color.pack()
                hue += 1
        pixels.show()
        time.sleep(wait)


def frontback():
    global hue
    wait = 0.1
    for y in range(4):
        for x in range(4):
            for z in range(4):
                i = XYZ(x, y, z)
                color = fancy.CHSV(hue % 255)
                color = fancy.gamma_adjust(color, brightness=brightness)
                pixels[i] = color.pack()
                hue += 1
        pixels.show()
        time.sleep(wait)

def diagonal():
    global hue
    wait = 0.02
    for i in range(4):
        for y in range(i+1):
            for x in range(i,-1,-1):
                for z in range(4):
                    pos = XYZ(x, y, z)
                    color = fancy.CHSV(hue % 255)
                    color = fancy.gamma_adjust(color, brightness=brightness)
                    pixels[pos] = color.pack()
                    hue += 1
        pixels.show()
        # time.sleep(wait)
    for i in range(3):
        for y in range(i+1,4):
            for x in range(3,i,-1):
                for z in range(4):
                    pos = XYZ(x, y, z)
                    color = fancy.CHSV(hue % 255)
                    color = fancy.gamma_adjust(color, brightness=brightness)
                    pixels[pos] = color.pack()
                    hue += 1
        pixels.show()
        # time.sleep(wait)

def expand():
    global hue
    wait = 0.1
    for size in range(4):
        for x in range(size+1):
            for y in range(size+1):
                for z in range(size+1):
                    i = XYZ(x, y, z)
                    color = fancy.CHSV(hue % 255)
                    color = fancy.gamma_adjust(color, brightness=brightness)
                    pixels[i] = color.pack()
                    hue += 1
        pixels.show()
        time.sleep(wait)


def move_layers(repeat):
    for i in range(repeat):
        updown()
        blank()
        leftright()
        blank()
        frontback()
        blank()


def rain():
    wait = 0.08
    nSteps = 100
    p_new = 0.3
    global hue
    drops_old = []
    drops_new = []
    for i in range(nSteps):
        for drop in drops_old:  # update drop positions
            i = XYZ(drop[0], drop[1], drop[2])
            pixels[i] = (0, 0, 0)  # remove old dot
            if drop[2] > 0:
                drop[2] -= 1
                drops_new.append([drop[0], drop[1], drop[2]])  # update list
                i = XYZ(drop[0], drop[1], drop[2])
                color = fancy.CHSV(hue % 255)
                color = fancy.gamma_adjust(color, brightness=brightness)
                pixels[i] = color.pack()
        if random.random() > p_new:  # generate new drop
            x = random.randint(0, 3)
            y = random.randint(0, 3)
            drops_new.append([x, y, 3])
            i = XYZ(x, y, 3)
            color = fancy.CHSV(hue % 255)
            color = fancy.gamma_adjust(color, brightness=brightness)
            pixels[i] = color.pack()
        drops_old = drops_new.copy()
        drops_new.clear()
        pixels.show()
        time.sleep(wait)
        hue += 1


def blank():
    pixels.fill((0, 0, 0))
    pixels.show()


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)


def rainbow_cycle():
    global hue
    wait = 0.05
    for i in range(num_pixels):
        color = fancy.CHSV(hue % 255)
        color = fancy.gamma_adjust(color, brightness=brightness)
        pixels[i] = color.pack()
        pixels.show()
        time.sleep(wait)
        hue += 4


def colorcycle():
    global hue
    for j in range(255):
        color = fancy.CHSV(hue % 255)
        color = fancy.gamma_adjust(color, brightness=brightness)
        pixels.fill(color.pack())
        pixels.show()
        # time.sleep(wait)
        hue += 2


while True:
    blank()
    time.sleep(1)
    # diagonal()
    blank()
    rainbow_cycle()
    blank()
    move_layers(4)
    blank()
    rain()
    blank()
    colorcycle()
    blank()
