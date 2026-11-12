"""Marching Words: a tiny marquee for the PixelWing's 10 x 5 LEDs."""
import time
import board
import neopixel
from digitalio import DigitalInOut, Direction
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.sparkle import Sparkle

# ESP32-S3 DevKitM pin names; PixelWing-specific aliases require its custom build.
PIXEL_PIN = board.IO48
STATUS_LED_PIN = board.IO35

WIDTH = 10
HEIGHT = 5
BRIGHTNESS = 0.1
SCROLL_SECONDS = 0.12  # Seconds per column; smaller is faster.
FLIP_X = True
FLIP_Y = False
SERPENTINE = False  # Existing board demo uses sequential rows.

RED = (255, 20, 15)
GREEN = (0, 180, 25)
GOLD = (255, 150, 0)
BLUE = (20, 70, 255)
WHITE = (180, 180, 180)
BLACK = (0, 0, 0)

# Three columns by five rows: each character fits this short display.
FONT = {
    ' ': ('000', '000', '000', '000', '000'),
    'A': ('010', '101', '111', '101', '101'),
    'B': ('110', '101', '110', '101', '110'),
    'C': ('011', '100', '100', '100', '011'),
    'D': ('110', '101', '101', '101', '110'),
    'E': ('111', '100', '110', '100', '111'),
    'F': ('111', '100', '110', '100', '100'),
    'G': ('011', '100', '101', '101', '011'),
    'H': ('101', '101', '111', '101', '101'),
    'I': ('111', '010', '010', '010', '111'),
    'J': ('001', '001', '001', '101', '010'),
    'K': ('101', '101', '110', '101', '101'),
    'L': ('100', '100', '100', '100', '111'),
    'M': ('101', '111', '111', '101', '101'),
    'N': ('101', '111', '111', '111', '101'),
    'O': ('010', '101', '101', '101', '010'),
    'P': ('110', '101', '110', '100', '100'),
    'Q': ('010', '101', '101', '111', '011'),
    'R': ('110', '101', '110', '101', '101'),
    'S': ('011', '100', '010', '001', '110'),
    'T': ('111', '010', '010', '010', '010'),
    'U': ('101', '101', '101', '101', '111'),
    'V': ('101', '101', '101', '101', '010'),
    'W': ('101', '101', '111', '111', '101'),
    'X': ('101', '101', '010', '101', '101'),
    'Y': ('101', '101', '010', '010', '010'),
    'Z': ('111', '001', '010', '100', '111'),
    '0': ('111', '101', '101', '101', '111'),
    '1': ('010', '110', '010', '010', '111'),
    '2': ('110', '001', '010', '100', '111'),
    '3': ('110', '001', '010', '001', '110'),
    '4': ('101', '101', '111', '001', '001'),
    '5': ('111', '100', '110', '001', '110'),
    '6': ('011', '100', '111', '101', '111'),
    '7': ('111', '001', '010', '010', '010'),
    '8': ('111', '101', '111', '101', '111'),
    '9': ('111', '101', '111', '001', '110'),
    '!': ('010', '010', '010', '000', '010'),
    '?': ('110', '001', '010', '000', '010'),
    '.': ('000', '000', '000', '000', '010'),
    '-': ('000', '000', '111', '000', '000'),
}

# Palette-indexed sprites; add your own five-row shapes here.
SHAPES = {
    'tree': ('0000100000', '0001210000', '0011121000',
             '0112111100', '0000300000'),
    'heart': ('0011011000', '0111111100', '0111111100',
              '0011111000', '0001110000'),
}
TREE_PALETTE = (BLACK, GREEN, RED, GOLD)
HEART_PALETTE = (BLACK, RED)

# Each entry is (scene type, text/shape/effect, color/palette, seconds).
# Text duration is determined by its length and SCROLL_SECONDS.
PLAYLIST = (
    ('text', 'HELLO WORLD!', BLUE, 0),
    ('effect', 'comet', GOLD, 2.0),
    ('text', 'MERRY CHRISTMAS!', RED, 0),
    ('shape', 'tree', TREE_PALETTE, 4.0),
    ('effect', 'sparkle', WHITE, 2.0),
    ('text', 'JOY LOVE PEACE', GREEN, 0),
    ('shape', 'heart', HEART_PALETTE, 2.0),
)


def pixel_index(x, y):
    if FLIP_X:
        x = WIDTH - 1 - x
    if FLIP_Y:
        y = HEIGHT - 1 - y
    if SERPENTINE and y % 2:
        x = WIDTH - 1 - x
    return y * WIDTH + x


def draw_text(pixels, message, offset, color):
    pixels.fill(BLACK)
    # Only visit characters intersecting the display, regardless of text length.
    first = max(0, (-offset) // 4)
    last = min(len(message), (WIDTH - 1 - offset) // 4 + 1)
    for position in range(first, last):
        glyph = FONT.get(message[position], FONT['?'])
        left = offset + position * 4
        for y, row in enumerate(glyph):
            for dx, bit in enumerate(row):
                x = left + dx
                if 0 <= x < WIDTH and bit == '1':
                    pixels[pixel_index(x, y)] = color
    pixels.show()


def scroll_text(pixels, message, color):
    message = message.upper()
    for offset in range(WIDTH, -len(message) * 4 - 1, -1):
        draw_text(pixels, message, offset, color)
        time.sleep(SCROLL_SECONDS)


def show_shape(pixels, name, palette, seconds):
    deadline = time.monotonic() + seconds
    frame = 0
    while time.monotonic() < deadline:
        pixels.fill(BLACK)
        for y, row in enumerate(SHAPES[name]):
            for x, value in enumerate(row):
                color = palette[int(value)]
                # Alternate the tree ornaments between red and gold.
                if name == 'tree' and value == '2':
                    color = RED if (frame + x + y) % 2 else GOLD
                pixels[pixel_index(x, y)] = color
        pixels.show()
        frame += 1
        time.sleep(0.25)


def show_effect(pixels, name, color, seconds):
    pixels.fill(BLACK)
    if name == 'comet':
        animation = Comet(pixels, speed=0.03, color=color, tail_length=8)
    elif name == 'sparkle':
        animation = Sparkle(pixels, speed=0.08, color=color)
    else:
        raise ValueError('Unknown effect: ' + name)
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        animation.animate()
        time.sleep(0.005)
    pixels.fill(BLACK)
    pixels.show()


def main():
    user_led = DigitalInOut(STATUS_LED_PIN)
    user_led.direction = Direction.OUTPUT
    user_led.value = False
    pixels = neopixel.NeoPixel(
        PIXEL_PIN, WIDTH * HEIGHT, brightness=BRIGHTNESS, auto_write=False
    )
    print('Marching Words ready: edit PLAYLIST to change the show.')
    try:
        while True:
            for kind, content, color, seconds in PLAYLIST:
                if kind == 'text':
                    scroll_text(pixels, content, color)
                elif kind == 'shape':
                    show_shape(pixels, content, color, seconds)
                elif kind == 'effect':
                    show_effect(pixels, content, color, seconds)
                else:
                    raise ValueError('Unknown scene: ' + kind)
    finally:
        pixels.fill(BLACK)
        pixels.show()
        pixels.deinit()
        user_led.deinit()


if __name__ == '__main__':
    main()
