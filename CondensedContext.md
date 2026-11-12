# CondensedContext

## Context Freshness
- Last Verified Commit: 6a99d8dc15aca57b24538ae0643597a0e3cdb130
- Current HEAD: 6a99d8dc15aca57b24538ae0643597a0e3cdb130
- Status: partial; starter implementation uncommitted (2026-11-12).

## Current Focus
- Scrolling text, small shapes, and Adafruit LED Animation transitions.

## Stable Facts
- PixelWing ESP32-S3: 10 × 5 sequential rows, matrix GPIO48, status LED GPIO35,
  brightness 0.1. Code now uses DevKitM board.IO48 and board.IO35 names.
- PixelWing-specific aliases require user's unofficial firmware build.
- Examples removed at user request; tilt demo exists in another project.

## Handoff
- Earlier marquee version installed on CIRCUITPY; latest pin changes are local only.
- User explicitly requested no upload of the changed code.py to PixelWing.
- Board console confirmed successful startup and execution inside a transition.
- Further 40-second console observation completed without runtime errors.
- User reported backward text; FLIP_X=True corrects horizontal orientation.
- Next: user confirms corrected orientation and chooses custom phrases.

## File Map
- code.py: 3×5 font, clipped scrolling, palette sprites, editable playlist,
  Adafruit Comet/Sparkle effects, orientation settings.
- README.md: setup, DevKitM pin mapping, playlist editing, shape format.

## Validation Memory
- Host checks passed: syntax, font/sprite dimensions, palette bounds, scroll
  clipping, and bijective pixel mapping for every orientation setting.
- No additional libraries installed; existing board libraries used.
- Serial console uses standard-library os/select/termios; host lacks pyserial.
- Pin update: syntax passed; IO35/IO48 confirmed against local CircuitPython
  espressif_esp32s3_devkitm_1_n8/pins.c. No hardware run of changed code.

## Recent Changes
- 2026-11-12: Switched to generic DevKitM GPIO aliases; removed examples and
  restoration docs. Repository changes only; no device upload.
- 2026-11-12: Added marquee starter, backed up original demo, installed to board.

## Open Threads
- Confirm physical text orientation on the board.
