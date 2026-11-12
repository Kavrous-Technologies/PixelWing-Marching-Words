# PixelWing Marching Words

A looping mini marquee for the PixelWing ESP32-S3's 10 × 5 NeoPixel matrix:
scrolling words, a twinkling Christmas tree, a heart, and Adafruit comet and
sparkle transitions.

## Run

Copy `code.py` to the connected `CIRCUITPY` drive. CircuitPython automatically
restarts the show when the file is saved. The connected board already has the
required libraries; for a fresh setup, put `neopixel.mpy` and the
`adafruit_led_animation` folder from a matching CircuitPython library bundle
in `CIRCUITPY/lib/`.

The code uses ESP32-S3 DevKitM CircuitPython pin names: `board.IO48` for the
PixelWing matrix data and `board.IO35` for its status LED. PixelWing-specific
`board.NEOPIXEL` and `board.LED` aliases depend on the unofficial PixelWing
build; this program uses the generic GPIO names instead. Use firmware suitable
for your board's flash and PSRAM configuration.

The matrix has 50 LEDs, sequential rows of 10, and brightness `0.1`. The status
LED is turned off. The accelerometer is not needed for this show.

## Make it yours

Edit `PLAYLIST` in `code.py`. Each entry contains a scene type, content,
color or palette, and duration in seconds:

```python
('text', 'HAPPY HOLIDAYS!', GOLD, 0),
('shape', 'tree', TREE_PALETTE, 4.0),
('effect', 'sparkle', WHITE, 2.0),
```

Text scrolls completely across the matrix; its duration follows its length.
`SCROLL_SECONDS` controls the time per column. The font supports A–Z, digits,
spaces, and `! ? . -`; lowercase is converted to uppercase and other symbols
appear as question marks.

Shapes are five strings of ten palette indices in `SHAPES`. Zero is the
background. Add a shape and a corresponding palette, then reference it in the
playlist. The tree's ornaments alternate red and gold.

If the words appear mirrored or upside down, set `FLIP_X` or `FLIP_Y`.
`SERPENTINE` supports alternating row wiring; leave it false for this board.
Comet transitions follow physical pixel order.

The transitions use the installed [Adafruit LED Animation library](https://docs.circuitpython.org/projects/led-animation/en/latest/api.html).
