import time
from rainbowio import colorwheel
import random


def fill(color):
    def _fill(pixels, speed):
        for i in range(pixels.n):
            pixels[i] = color
        pixels.show()
        time.sleep(speed)

    return _fill


def rainbow(pixels, speed):
    for j in range(255):
        for i in range(pixels.n):
            pixel_index = (i * 256 // pixels.n) + j
            pixels[i] = colorwheel(pixel_index & 255)
        pixels.show()
        time.sleep(speed)


def fade(color: tuple[int, int, int], step=0.01):
    initialised = False
    change = -step
    modifier = 1.0

    def _fade(pixels, speed):
        nonlocal initialised, change, modifier

        if not initialised:
            for i in range(pixels.n):
                pixels[i] = color

            initialised = True

        else:
            modifier += change
            if modifier < 0:
                modifier = 0
                change = -change

            if modifier > 1:
                modifier = 1
                change = -change

            for i in range(pixels.n):
                pixels[i] = tuple(map(lambda j: j * modifier, color))

            pixels.show()
            time.sleep(speed)

    return _fade


def twinkle(color: tuple[int, int, int], step=0.01):
    initialised = False
    changes = []
    modifiers = []

    def _twinkle(pixels, speed):
        nonlocal initialised, changes, modifiers

        if not initialised:
            modifiers = [random.random() for _ in range(pixels.n)]
            changes = [random.choice([step, -step]) for _ in range(pixels.n)]

            for i in range(pixels.n):
                pixels[i] = tuple(map(lambda j: j * modifiers[i], color))

            initialised = True

        else:
            for i in range(pixels.n):
                modifiers[i] += changes[i]

                if modifiers[i] < 0:
                    modifiers[i] = 0
                    changes[i] = -changes[i]

                if modifiers[i] > 1:
                    modifiers[i] = 1
                    changes[i] = -changes[i]

                pixels[i] = tuple(map(lambda j: j * modifiers[i], color))

            pixels.show()
            time.sleep(speed)

    return _twinkle
